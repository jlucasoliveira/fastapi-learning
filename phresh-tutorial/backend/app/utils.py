import logging

logger = logging.getLogger(__name__)


def handle_exception(message: str, error: Exception):
    logger.warning(f"=== {message} ERROR ===")
    logger.error(error)
    logger.warning(f"=== {message} ERROR ===")
