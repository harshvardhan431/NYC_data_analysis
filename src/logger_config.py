import logging
import sys


def setup_logger(name: str = __name__) -> logging.Logger:
    logger = logging.getLogger(name)

    # Prevent duplicate handlers if function is called multiple times for the same logger name
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)

    # CRITICAL: Prevent logs from bubbling up to the root logger (prevents double logging)
    logger.propagate = False

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )

    # 1. Console Handler (explicitly output to stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 2. File Handler (with error handling)
    try:
        file_handler = logging.FileHandler("pipeline.log", mode="a")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except (PermissionError, OSError) as e:
        logger.warning(f"Failed to attach file handler for pipeline.log: {e}")

    return logger