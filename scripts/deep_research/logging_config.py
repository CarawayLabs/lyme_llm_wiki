"""Logging setup for Deep Research CLI runs."""

from __future__ import annotations

import logging
import sys


def configure_logging(level: str) -> None:
    """Configure readable console logging."""

    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
    )
