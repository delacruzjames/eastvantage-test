"""Application logging setup."""

import logging
from logging.config import dictConfig

from app.config import settings

LOG_FORMAT = "%(asctime)s %(levelname)-8s %(name)s: %(message)s"


def configure_logging() -> None:
    """Send application and uvicorn logs through one consistent formatter."""
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": LOG_FORMAT,
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "standard",
                    "stream": "ext://sys.stdout",
                },
            },
            "root": {
                "handlers": ["console"],
                "level": settings.log_level,
            },
            "loggers": {
                "uvicorn": {"handlers": ["console"], "level": settings.log_level, "propagate": False},
                "uvicorn.error": {
                    "handlers": ["console"],
                    "level": settings.log_level,
                    "propagate": False,
                },
                # Request lines are already logged by our own middleware.
                "uvicorn.access": {"handlers": ["console"], "level": "WARNING", "propagate": False},
            },
        }
    )


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
