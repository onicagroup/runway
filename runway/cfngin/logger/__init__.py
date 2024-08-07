"""CFNgin logger."""

from __future__ import annotations

import logging
import sys
from typing import Any

DEBUG_FORMAT = (
    "[%(asctime)s] %(levelname)s %(threadName)s %(name)s:%(lineno)d(%(funcName)s): %(message)s"
)
INFO_FORMAT = "[%(asctime)s] %(message)s"
COLOR_FORMAT = "[%(asctime)s] \033[%(color)sm%(message)s\033[39m"

ISO_8601 = "%Y-%m-%dT%H:%M:%S"


class ColorFormatter(logging.Formatter):
    """Handles colorizing formatted log messages if color provided."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log message."""
        if "color" not in record.__dict__:
            record.__dict__["color"] = 37
        return super().format(record)


def setup_logging(verbosity: int, formats: dict[str, Any] | None = None) -> None:
    """Configure a proper logger based on verbosity and optional log formats.

    Args:
        verbosity: 0, 1, 2
        formats: Keys (``info``, ``color``, ``debug``) which may override the
            associated default log formats.

    """
    if formats is None:
        formats = {}

    log_level = logging.INFO

    log_format = formats.get("info", INFO_FORMAT)

    if sys.stdout.isatty():
        log_format = formats.get("color", COLOR_FORMAT)

    if verbosity > 0:
        log_level = logging.DEBUG
        log_format = formats.get("debug", DEBUG_FORMAT)

    if verbosity < 2:
        logging.getLogger("botocore").setLevel(logging.CRITICAL)

    hdlr = logging.StreamHandler()
    hdlr.setFormatter(ColorFormatter(log_format, ISO_8601))
    logging.root.addHandler(hdlr)
    logging.root.setLevel(log_level)
