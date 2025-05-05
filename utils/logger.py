""" Logger setup for web scrapers"""
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name: str,
        log_file: str = "logs/scraper.log",
        level=logging.INFO
    ) -> logging.Logger:
    """
    Sets up and returns a logger with a rotating file handler.

    Args:
        name (str): Name of the logger.
        log_file (str): Path to the log file.
        level: Logging level (e.g., logging.INFO, logging.DEBUG).

    Returns:
        logging.Logger: Configured logger instance.
    """
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] - %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5_000_000,
        backupCount=3
    )
    file_handler.setFormatter(formatter)

    # Avoid duplicate handlers
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger