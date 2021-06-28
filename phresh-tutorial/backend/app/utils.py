import logging

logger = logging.getLogger(__name__)


def handle_exception(message: str, error: Exception):
    logger.warn(f"=== {message} ERROR ===")
    logger.error(error)
    logger.warn(f"=== {message} ERROR ===")
