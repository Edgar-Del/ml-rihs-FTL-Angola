import logging
import time
from functools import wraps
from typing import Any, Callable


def setup_logging() -> None:
    """Configura o logging padrão da aplicação."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def timing_decorator(func: Callable) -> Callable:
    """Decorator para medir tempo de execução de funções síncronas."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time
        logging.info("%s executado em %.4f segundos", func.__name__, duration)
        return result

    return wrapper

