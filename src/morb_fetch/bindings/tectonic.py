import logging
import sys
import platform
import pooch

from morb_fetch.config import get_config

logger = logging.getLogger("morb_fetch")
pooch_logger = pooch.get_logger()
pooch_logger.setLevel("WARNING")


class TectonicDownloader:
    """
    Download Tectonic binary from GitHub releases.
    Tectonic is a XELateX-implementation engine that can flexibly fetch related resources to compile LaTeX documents.

    NOTE: Tectonic does not implement the biber engine. Check `TectonicBiberDownloader` to retrieve the biber engine.
    """
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
            "win32": "pc",
            "darwin": "apple",
            "linux": "unknown"
        }
        # Architecture for each platform
        arch = platform.machine().lower()
        if arch in ['amd64', 'x86_64']:
            arch = 'x86_64'
        elif arch in ['arm64', 'aarch64']:
            arch = 'arm64'

        operating_system = platform.system().lower()
        # Generate filename
        filebase = BASE_FILENAME.format(
            version=version,
            arch=arch,
            machine=machine[sys.platform],
            os=operating_system
        )

        # Compiler
        compiler = {
            "win32": "msvc",
            "linux": "gnu"
        }
        if sys.platform != "darwin":
            filebase = f"{filebase}-{compiler[sys.platform]}"

        fileext = "zip" if sys.platform=="win32" else "tar.gz"
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
        exec = "tectonic.exe" if operating_system == "windows" else "tectonic"
        exec_path = unzip_path / exec
        logger.info(f"{cls.name}-{version} downloaded at {unzip_path}")

        return str(exec_path)


class TectonicBiberDownloader:
    """
    Download Biber binary from SourceForge releases.
    Add to OS's PATH for Tectonic to find the biber binary.
    """
    name = "biber"
    registry = [
        "2.15",
        "2.16",
        "2.17",
        "2.18",
        "2.19",
        "2.20",
        "2.21"
    ]
    download_path = get_config().tectonic_path
    REPO_URL = "https://sourceforge.net/projects/biblatex-biber"

    @classmethod
    def list_available_versions(cls) -> list[str]:
        """
        List all available versions of Tectonic
        """
        return cls.registry

    @classmethod
    def retrieve_version(cls, version: str) -> str:
        BASE_URL = (
            cls.REPO_URL
            + "/files/biblatex-biber/{version}/binaries/{os}/{filename}/download"
        )
        filename = "biber-{os}_{arch}.tar.gz".format(
            os=sys.platform.lower(),
            arch=platform.machine().lower()
        )
        url = BASE_URL.format(
            version=version,
            os=sys.platform.capitalize(),
            arch=platform.machine().lower(),
            filename=filename
        )
        extract_dir = cls.download_path / f"{cls.name}-{version}"
        pooch.retrieve(
            url=url,
            fname=f"biber-{version}.tar.gz",
            path=cls.download_path,
            processor=pooch.Untar(extract_dir=extract_dir),
            progressbar=True,
            known_hash=None
        )

        unzip_path = cls.download_path / extract_dir

        return str(unzip_path)
