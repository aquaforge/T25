
"""различные функции"""
import logging
import logging.handlers
from logging.handlers import RotatingFileHandler
from logging import StreamHandler
import os
import sys


def init_logging(log_level: str = 'WARNING', log_dir: str = 'tmp'):
    """активация логгера logging"""
    os.makedirs(log_dir, exist_ok=True)
    log_handlers = [
        RotatingFileHandler(
            filename=f"{log_dir}\\main.log", mode="a", maxBytes=500_000, backupCount=10),
        StreamHandler(stream=sys.stdout)
    ]

    logging.basicConfig(level=log_level.upper(),
                        handlers=log_handlers,
                        format="%(asctime)s|%(levelname)s|%(funcName)s:%(lineno)d|%(message)s")
