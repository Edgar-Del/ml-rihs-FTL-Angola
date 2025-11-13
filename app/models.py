from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict

import numpy as np

from app.utils.feature_aliases import CANONICAL_FEATURES
from app.utils.validation import (
    ensure_only_known_features,
    normalize_features,
    validate_feature_payload,
)
from ml.model_loader import load_metadata, load_model

logger = logging.getLogger(__name__)


class SustainabilityModel:
    """Classe para gerenciar o ciclo de vida do modelo de sustentabilidade."""
    
    def __init__(self) -> None:
        self.model = None
        self.feature_names = CANONICAL_FEATURES
        self.class_labels = {
            0: "Muito Baixo",
            1: "Baixo",
            2: "Médio",
            3: "Alto",
            4: "Muito Alto",
        }
        self.metadata: Dict[str, Any] = {}
        self.model_version: str = "desconhecido"
        self.loaded_path: Path | None = None

    def load(self, model_path: str, metadata_path: str) -> bool:
        try:
            loaded_obj, resolved_path = load_model(model_path)
            self.loaded_path = resolved_path
            
            # Tenta extrair o modelo se for um dicionário
            if isinstance(loaded_obj, dict):
                logger.info(f"Objeto carregado é um dicionário com chaves: {list(loaded_obj.keys())}")
                # Procura por chaves comuns que podem conter o modelo
                possible_keys = ['model', 'pipeline', 'classifier', 'estimator', 'modelo', 'final_model']
                model_obj = None
                for key in possible_keys:
                    if key in loaded_obj:
                        candidate = loaded_obj[key]
                        logger.info(f"Verificando chave '{key}': tipo={type(candidate).__name__}, tem predict={hasattr(candidate, 'predict')}, tem predict_proba={hasattr(candidate, 'predict_proba')}")
                        
                        # Se for uma Pipeline do sklearn, ela mesma tem os métodos
                        if hasattr(candidate, "predict") and hasattr(candidate, "predict_proba"):
                            model_obj = candidate
                            logger.info(f"✓ Modelo válido encontrado na chave '{key}' do dicionário")
                            break
                        # Se for uma Pipeline, verifica o último step
                        elif hasattr(candidate, "steps") and len(candidate.steps) > 0:
                            final_step = candidate.steps[-1][1]
                            if hasattr(final_step, "predict") and hasattr(final_step, "predict_proba"):
                                model_obj = candidate  # Usa a pipeline completa
                                logger.info(f"✓ Pipeline encontrada na chave '{key}' com estimador válido")
                                break
                
                # Se não encontrou em chaves específicas, tenta o primeiro valor que seja um modelo
                if model_obj is None or not (hasattr(model_obj, "predict") and hasattr(model_obj, "predict_proba")):
                    logger.info("Procurando modelo em todos os valores do dicionário...")
                    for key, value in loaded_obj.items():
                        # Verifica se é um modelo direto
                        if hasattr(value, "predict") and hasattr(value, "predict_proba"):
                            model_obj = value
                            logger.info(f"✓ Modelo encontrado na chave '{key}' do dicionário")
                            break
                        # Verifica se é uma Pipeline
                        elif hasattr(value, "steps") and len(value.steps) > 0:
                            final_step = value.steps[-1][1]
                            if hasattr(final_step, "predict") and hasattr(final_step, "predict_proba"):
                                model_obj = value
                                logger.info(f"✓ Pipeline encontrada na chave '{key}'")
                                break
                
                if model_obj is None or not (hasattr(model_obj, "predict") and hasattr(model_obj, "predict_proba")):
                    logger.error("❌ Dicionário carregado não contém um modelo válido")
                    logger.error(f"Chaves disponíveis: {list(loaded_obj.keys())}")
                    for key, value in loaded_obj.items():
                        value_type = type(value).__name__
                        has_predict = hasattr(value, 'predict')
                        has_predict_proba = hasattr(value, 'predict_proba')
                        has_steps = hasattr(value, 'steps')
                        logger.error(f"  {key}: {value_type} (predict={has_predict}, predict_proba={has_predict_proba}, steps={has_steps})")
                    
                    # Se o dicionário contém apenas metadados, tenta carregar outros arquivos
                    if set(loaded_obj.keys()).issubset({'features', 'feature_importance', 'performance', 'class_names'}):
                        logger.warning("Arquivo contém apenas metadados, tentando carregar outros modelos...")
                        # Tenta outros arquivos na mesma pasta
                        model_dir = resolved_path.parent
                        alternative_files = [
                            model_dir / "hotel_sustainability_classifier_model.pkl",
                            model_dir / "sustainability_classifier_complete.pkl",
                            model_dir / "model_1.pkl",
                            model_dir / "rihs_model_01.pkl",
                        ]
                        
                        found_alternative = False
                        for alt_file in alternative_files:
                            if alt_file.exists():
                                try:
                                    logger.info(f"Tentando carregar: {alt_file.name}")
                                    alt_obj, alt_path = load_model(str(alt_file))
                                    
                                    # Verifica se é um modelo válido
                                    if isinstance(alt_obj, dict):
                                        # Tenta extrair o modelo do dicionário
                                        if 'model' in alt_obj and hasattr(alt_obj['model'], 'predict'):
                                            logger.info(f"✓ Modelo encontrado em {alt_file.name}")
                                            loaded_obj = alt_obj['model']
                                            resolved_path = alt_path
                                            found_alternative = True
                                            break
                                    elif hasattr(alt_obj, 'predict') and hasattr(alt_obj, 'predict_proba'):
                                        logger.info(f"✓ Modelo válido encontrado em {alt_file.name}")
                                        loaded_obj = alt_obj
                                        resolved_path = alt_path
                                        found_alternative = True
                                        break
                                except Exception as alt_exc:
                                    logger.warning(f"Falha ao carregar {alt_file.name}: {alt_exc}")
                                    continue
                        
                        # Se não encontrou alternativa, retorna False
                        if not found_alternative:
                            self.model = None
                            return False
                    else:
                        self.model = None
                        return False
                else:
                    loaded_obj = model_obj
            
            # Verifica se é uma Pipeline do sklearn (mesmo que não seja dict)
            elif hasattr(loaded_obj, "steps") and len(loaded_obj.steps) > 0:
                logger.info(f"Objeto carregado é uma Pipeline com {len(loaded_obj.steps)} steps")
                # Pipeline do sklearn já tem os métodos predict e predict_proba
                if not (hasattr(loaded_obj, "predict") and hasattr(loaded_obj, "predict_proba")):
                    logger.error("Pipeline não tem métodos predict/predict_proba")
                    self.model = None
                    return False
                logger.info("✓ Pipeline válida detectada")
            
            # Valida que o objeto carregado tem métodos de predição
            if not hasattr(loaded_obj, "predict") or not hasattr(loaded_obj, "predict_proba"):
                logger.error("Objeto carregado não é um modelo válido (sem métodos predict/predict_proba)")
                logger.error(f"Tipo do objeto: {type(loaded_obj).__name__}")
                logger.error(f"Atributos disponíveis: {[a for a in dir(loaded_obj) if not a.startswith('_')][:10]}")
                self.model = None
                return False
            
            self.model = loaded_obj
            metadata = load_metadata(metadata_path)
            selected_metadata = metadata
            version = metadata.get("version", "unknown")

            models_info = metadata.get("models")
            if isinstance(models_info, dict):
                for candidate_version, info in models_info.items():
                    artifact = info.get("artifact_path")
                    if artifact and Path(artifact).resolve() == resolved_path.resolve():
                        selected_metadata = {**info, "version": candidate_version}
                        version = candidate_version
                        break
                else:
                    default_version = metadata.get("default_version")
                    if default_version and default_version in models_info:
                        info = models_info[default_version]
                        selected_metadata = {**info, "version": default_version}
                        version = default_version

            self.metadata = selected_metadata
            self.model_version = version
            return True
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("Erro ao carregar modelo principal: %s", exc)
            self.model = None
            return False
    
    def predict(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Realiza uma predição a partir de um payload de features."""
        if not self.is_loaded():
            raise RuntimeError("Modelo não está carregado.")

        normalized_features = normalize_features(payload)
        ensure_only_known_features(normalized_features)
        validate_feature_payload(normalized_features)

        feature_vector = np.array(
            [[normalized_features[feature] for feature in self.feature_names]]
        )

        prediction = int(self.model.predict(feature_vector)[0])
        probabilities_array = self.model.predict_proba(feature_vector)[0]
        probabilities = probabilities_array.tolist()
        prediction_label = self.class_labels.get(prediction, "Desconhecido")
        
        # Calcula a confiança (probabilidade da classe predita)
        confidence = float(probabilities_array[prediction]) * 100.0
        
        # Mapeia todas as probabilidades para os nomes das classes
        all_probabilities = {
            self.class_labels.get(i, f"Classe {i}"): float(prob) 
            for i, prob in enumerate(probabilities)
        }

        return {
            "prediction": prediction,
            "probabilities": probabilities,
            "prediction_label": prediction_label,
            "confidence": round(confidence, 2),
            "all_probabilities": all_probabilities,
            "model_version": self.model_version,
        }
    
    def is_loaded(self) -> bool:
        """Verifica se o modelo está carregado."""
        return self.model is not None