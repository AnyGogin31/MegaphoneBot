import logging
from logging.handlers import TimedRotatingFileHandler

from pathlib import Path

import sys


def configure_logging() -> None:
    logs_dir = Path("logs")
    logs_dir.mkdir(parents=True,exist_ok=True)

    log_file_path = logs_dir / "now.log"

    log_format = (
        "%(asctime)s | %(levelname)-8s | "
        "%(filename)s:%(funcName)s:%(lineno)d - %(message)s"
    )
    date_format = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(log_format, date_format)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    file_handler = TimedRotatingFileHandler(
        filename=log_file_path,
        when="midnight",
        encoding="utf-8"
    )

    file_handler.suffix = "%d_%m_%Y.log"
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    logging.basicConfig(
        level=logging.INFO,
        handlers=[
            console_handler,
            file_handler
        ]
    )


def get_logger(name) -> logging.Logger:
    return logging.getLogger(name)
