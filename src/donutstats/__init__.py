from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

from .donutstats import (
    DonutStats,
    DonutSMPError,
    UnauthorizedRequest,
    RateLimited,
    UnexpectedError
)

__all__ = [
    "DonutStats",
    "DonutSMPError",
    "UnauthorizedRequest",
    "RateLimited",
    "UnexpectedError",
]

try:
    __version__ = version("donutstats")
except PackageNotFoundError:  # not installed (e.g. running from source tree)
    __version__ = "0.0.0"
