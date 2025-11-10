import logging
import time
from functools import wraps
from typing import Any, Callable


def setup_logging():
    """Configura o logging da aplicação"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def timing_decorator(func: Callable) -> Callable:
    """Decorator para medir tempo de execução"""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        logging.info(f"{func.__name__} executado em {end_time - start_time:.4f} segundos")
        return result
    return wrapper


def validate_features(features: dict, required_features: list) -> bool:
    """
    Valida se todas as features necessárias estão presentes
    
    Args:
        features: Dicionário com features
        required_features: Lista de features obrigatórias
        
    Returns:
        bool: True se válido
    """
    missing = [feature for feature in required_features if feature not in features]
    if missing:
        logging.warning(f"Features missing: {missing}")
        return False
    return True