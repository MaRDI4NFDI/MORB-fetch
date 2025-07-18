import logging
import sys
import platform
import pooch

from morb_fetch.config import get_config

logger = logging.getLogger("morb_fetch")
pooch_logger = pooch.get_logger()
pooch_logger.setLevel("WARNING")


class TectonicDownloader:
    name = "tectonic"
    registry = [
        "0.15.0"
    ]
    download_path = get_config().tectonic_path
    REPO_URL = "https://github.com/tectonic-typesetting/tectonic"

    @classmethod
    def list_available_versions(cls) -> list[str]:
        """
        List all available versions of Tectonic
        """
        return cls.registry

    @classmethod
    def retrieve_version(cls, version: str) -> str:
        """
        Retrieve a specific version of Tectonic
        """
        # URL format
        BASE_URL = cls.REPO_URL + "/releases/download/tectonic@{version}/{filename}"

        # Filename format
        BASE_FILENAME='tectonic-{version}-{arch}-{machine}-{os}'
        # Machine name for each platform
        machine = {
            "windows": "pc",
            "darwin": "apple",
            "linux": "unknown"
        }

        # Generate filename
        filebase = BASE_FILENAME.format(
            version=version,
            arch=platform.machine(),
            machine=machine[sys.platform],
            os=sys.platform
        )
        filebase = filebase + "-gnu" if sys.platform != "darwin" else filebase
        fileext = "zip" if sys.platform=="windows" else "tar.gz"
        filename = f"{filebase}.{fileext}"

        # Generate URL
        url = BASE_URL.format(
            version=version,
            filename=filename
        )

        # Post download extraction
        extract_dir = f"{cls.name}-{version}"
        postprocessor = (
            pooch.Untar(extract_dir=extract_dir)
            if fileext == "tar.gz"
            else pooch.Unzip(extract_dir=extract_dir)
        )

        # Download file
        pooch.retrieve(
            url=url,
            path=cls.download_path,
            fname=filename,
            known_hash=None,
            progressbar=True,
            processor=postprocessor
        )
        unzip_path = cls.download_path / extract_dir
        exec_path = unzip_path / "tectonic"
        logger.info(f"{cls.name}-{version} downloaded at {unzip_path}")

        return str(exec_path)
