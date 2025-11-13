from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict

import joblib

FALLBACK_MODEL_PATH = Path("./models/baseline/model.pkl")
FALLBACK_METADATA: Dict[str, Any] = {
    "version": "fallback",
    "metrics": {"info": "fallback model in-memory"},
}


def load_model(path: str):
    target = Path(path)
    try:
        model = joblib.load(target)
        logging.info("Model loaded from %s", target)
        return model, target
    except FileNotFoundError:
        logging.warning("Model not found at %s, attempting fallback...", target)
        # Tenta carregar sustainability_classification_pipeline.pkl no mesmo diretório
        pipeline_path = target.parent / "sustainability_classification_pipeline.pkl"
        if pipeline_path.exists():
            fallback = joblib.load(pipeline_path)
            logging.info("Fallback model loaded from %s", pipeline_path)
            return fallback, pipeline_path
        # Tenta carregar rihs_model.pkl no mesmo diretório
        rihs_model_path = target.parent / "rihs_model.pkl"
        if rihs_model_path.exists():
            fallback = joblib.load(rihs_model_path)
            logging.info("Fallback model loaded from %s", rihs_model_path)
            return fallback, rihs_model_path
        # Se rihs_model.pkl não existir, tenta o fallback padrão
        if FALLBACK_MODEL_PATH.exists():
            fallback = joblib.load(FALLBACK_MODEL_PATH)
            logging.info("Fallback model loaded from %s", FALLBACK_MODEL_PATH)
            return fallback, FALLBACK_MODEL_PATH
        logging.error("Fallback model not found at %s, %s or %s", pipeline_path, rihs_model_path, FALLBACK_MODEL_PATH)
        raise
    except Exception as exc:  # pylint: disable=broad-except
        logging.warning("Model loading failed: %s, attempting fallback...", exc)
        # Tenta carregar sustainability_classification_pipeline.pkl no mesmo diretório
        pipeline_path = target.parent / "sustainability_classification_pipeline.pkl"
        if pipeline_path.exists():
            try:
                fallback = joblib.load(pipeline_path)
                logging.info("Fallback model loaded from %s", pipeline_path)
                return fallback, pipeline_path
            except Exception as fallback_exc:  # pylint: disable=broad-except
                logging.warning("Fallback model also failed: %s", fallback_exc)
        # Tenta carregar rihs_model.pkl no mesmo diretório quando há erro de deserialização
        rihs_model_path = target.parent / "rihs_model.pkl"
        if rihs_model_path.exists():
            try:
                fallback = joblib.load(rihs_model_path)
                logging.info("Fallback model loaded from %s", rihs_model_path)
                return fallback, rihs_model_path
            except Exception as fallback_exc:  # pylint: disable=broad-except
                logging.warning("Fallback model also failed: %s", fallback_exc)
        # Se rihs_model.pkl falhar, tenta o fallback padrão
        if FALLBACK_MODEL_PATH.exists():
            try:
                fallback = joblib.load(FALLBACK_MODEL_PATH)
                logging.info("Fallback model loaded from %s", FALLBACK_MODEL_PATH)
                return fallback, FALLBACK_MODEL_PATH
            except Exception as fallback_exc:  # pylint: disable=broad-except
                logging.error("All fallback models failed: %s", fallback_exc)
        logging.error("Model loading failed: %s", exc)
        raise


def load_metadata(path: str) -> Dict[str, Any]:
    target = Path(path)
    if target.exists():
        try:
            with target.open(encoding="utf-8") as metadata_file:
                metadata = json.load(metadata_file)
                logging.info("Metadata loaded from %s", target)
                return metadata
        except Exception as exc:  # pylint: disable=broad-except
            logging.warning("Failed to load metadata from %s: %s", target, exc)
    else:
        logging.warning("Metadata file not found at %s", target)
    return FALLBACK_METADATA.copy()

