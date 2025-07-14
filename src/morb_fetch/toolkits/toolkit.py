import pooch
import logging
from typing import ClassVar
from pydantic import BaseModel
from pathlib import Path

from morb_fetch._types import DOIstr

logger = logging.getLogger("morb_fetch")
pooch_logger = pooch.get_logger()
pooch_logger.setLevel("WARNING")


class ToolkitDownloader(BaseModel):
    """
    Base Downloader class for Toolkits from Zenodo
    """
    name: ClassVar[str]
    registry: ClassVar[dict[str, DOIstr]]
    download_path: ClassVar[Path]

    @classmethod
    def list_available_versions(cls) -> list[str]:
        """
        List all available versions of MORLAB
        """
        return list(cls.registry.keys())

    @classmethod
    def retrieve_version(cls, version: str) -> str:
        """
        Retrieve a specific version of Toolkit
        """
        # assert that version is valid
        available_versions = cls.list_available_versions()
        if version not in available_versions:
            raise ValueError(f"Version {version} not found. Available versions: {available_versions}")

        # metadata
        doi = cls.registry[version]
        zip_filename = f"{cls.name}-{version}.zip"

        # build downloader from doi
        downloader = pooch.create(
            base_url=doi,
            path=cls.download_path,
            registry=None,
        )
        downloader.load_registry_from_doi()

        # fetch file
        downloader.fetch(
            fname=zip_filename,
            processor=pooch.Unzip(extract_dir='.'),
            progressbar=True,
        )

        unzip_path = cls.download_path / f"{cls.name}-{version}"
        logger.info(f"{cls.name}-{version} downloaded at {unzip_path}")

        return str(unzip_path)
