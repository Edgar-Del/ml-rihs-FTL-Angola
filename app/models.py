import joblib
import numpy as np
import logging
from typing import Dict, Any
import os

logger = logging.getLogger(__name__)


class SustainabilityModel:
    """Classe para gerenciar o modelo de sustentabilidade"""
    
    def __init__(self):
        self.model = None
        self.feature_names = [
            'price_per_night_usd', 'rating', 'avaliação_clientes', 'distância_do_centro_km',
            'energia_renovável', 'gestão_resíduos_índice', 'consumo_água_por_hóspede',
            'carbon_footprint_score', 'reciclagem_score', 'energia_limpa_score',
            'water_usage_index', 'sustainability_index', 'eco_impact_index', 'eco_value_ratio',
            'sentimento_score', 'eco_keyword_count', 'região_encoded',
            'possui_selo_sustentável_encoded', 'sentimento_sustentabilidade_encoded',
            'price_sust_ratio', 'eco_value_score', 'total_sust_score', 'price_category',
            'water_consumption_ratio'
        ]
        self.class_labels = {
            0: "Muito Baixa Sustentabilidade",
            1: "Baixa Sustentabilidade", 
            2: "Média Sustentabilidade",
            3: "Alta Sustentabilidade",
            4: "Muito Alta Sustentabilidade"
        }
    
    def load_model(self, model_path: str) -> bool:
        """
        Carrega o modelo do arquivo .pkl
        
        Args:
            model_path: Caminho para o arquivo do modelo
            
        Returns:
            bool: True se carregou com sucesso
        """
        try:
            logger.info(f"Carregando modelo de: {model_path}")
            
            if not os.path.exists(model_path):
                logger.error(f"Arquivo do modelo não encontrado: {model_path}")
                return False
            
            self.model = joblib.load(model_path)
            logger.info("Modelo carregado com sucesso!")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao carregar modelo: {str(e)}")
            return False
    
    def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Faz predição com base nas features
        
        Args:
            features: Dicionário com features do hotel
            
        Returns:
            Dict com predição e probabilidades
        """
        try:
            # Converte features para array na ordem correcta
            feature_array = np.array([[features[feature] for feature in self.feature_names]])
            
            # Faz predição
            prediction = self.model.predict(feature_array)[0]
            probabilities = self.model.predict_proba(feature_array)[0].tolist()
            
            # Obtém label
            prediction_label = self.class_labels.get(prediction, "Desconhecido")
            
            return {
                "prediction": int(prediction),
                "probabilities": probabilities,
                "prediction_label": prediction_label,
                "model_version": "1.0.0"
            }
            
        except Exception as e:
            logger.error(f"Erro durante predição: {str(e)}")
            raise e
    
    def is_loaded(self) -> bool:
        """Verifica se o modelo está carregado"""
        return self.model is not None