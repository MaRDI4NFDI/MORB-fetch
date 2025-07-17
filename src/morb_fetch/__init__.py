"""
Copyright (c) 2025 MORB Developers and Contributors. All rights reserved.

morb-fetch: Data Fetcher for MORB
"""

from morb_fetch.utils import loadmat, setup_logging

setup_logging()

from morb_fetch.config import Settings, print_config, get_config, clear_config
from morb_fetch.examples import (
    ABCType,
    ABCEType,
    ABCDEType,
    BCKMType,
    BCEKMType,
    DataSetType,
    DataSet,
    Matrix,
    Example,
    Database,
    get_database,
)
from morb_fetch.toolkits import (
    ToolkitDownloader,
    ZenodoToolkitDownloader,
    MORLABDownloader,
    MMESSDownloader,
    TectonicDownloader,
)


__all__ = [
    "Settings",
    "get_config",
    "clear_config",
    "print_config",
    "DataSetType",
    "DataSet",
    "Matrix",
    "ABCType",
    "ABCEType",
    "ABCDEType",
    "BCKMType",
    "BCEKMType",
    "Database",
    "Example",
    "ToolkitDownloader",
    "MORLABDownloader",
    "MMESSDownloader",
    "ZenodoToolkitDownloader",
    "TectonicDownloader",
    "get_database",
    "loadmat",
]
