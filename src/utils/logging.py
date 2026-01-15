#  MegaphoneBot
#  Copyright (C) 2026 AnyGogin31
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program. If not, see <https://www.gnu.org/licenses/>.

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
