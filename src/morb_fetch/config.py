import os
import logging
from rich.console import Console
from rich.table import Table
from rich import print
from typing import Optional
from pathlib import Path
from platformdirs import user_config_path, user_cache_path
from pydantic import AnyHttpUrl, TypeAdapter
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    PydanticBaseSettingsSource,
    YamlConfigSettingsSource,
)

from morb_fetch._types import SHA256Hash, CSVFilename, HumanFileSize, ConfigFilename

logger = logging.getLogger("morb_fetch")
logger.setLevel(logging.INFO)

# Find path for default morb_fetch.config.yaml file
config_path = Path.cwd()
config_filename = "morb_fetch.config.yaml"
local_config = config_path / config_filename
if local_config.exists():
    DEFAULT_CONFIG_FILE = local_config
else:
    config_path = user_config_path(appname="morb", appauthor="morb-users")
    global_config = config_path / config_filename
    DEFAULT_CONFIG_FILE = global_config

# Default CONFIG values
DEFAULT_SERVER_URL = "https://modelreduction.org/morb-data/"
DEFAULT_INDEXFILE = "examples.csv"
DEFAULT_INDEXFILEHASH = "sha256:39a07469c4b4952d66969288608cd1cccc3d86966456d7579b9dcf4b2383a54a"
DEFAULT_MAX_FILESIZE = None
DEFAULT_CACHE_PATH = user_cache_path(
    appname="morb", appauthor="morb-users", ensure_exists=True
)
DEFAULT_MMESS_PATH = DEFAULT_CACHE_PATH / "MMESS"
DEFAULT_MORLAB_PATH = DEFAULT_CACHE_PATH / "morlab"
DEFAULT_TECTONIC_PATH = DEFAULT_CACHE_PATH / "tectonic"

class Settings(BaseSettings):
    """
    Configuration settings for MORB-fetch.

    Attributes:
        serverurl (AnyHttpUrl): The base URL for the MORB-data server.
        indexfile (CSVFilename): The filename of the index file.
        indexfilehash (SHA256Hash): The SHA256 hash of the index file.
        max_filesize (Optional[HumanFileSize]): The maximum file size allowed.
        cache (Path): The path to the cache directory.
    """

    serverurl: AnyHttpUrl = AnyHttpUrl(DEFAULT_SERVER_URL)
    indexfile: CSVFilename = DEFAULT_INDEXFILE
    indexfilehash: SHA256Hash = DEFAULT_INDEXFILEHASH
    max_filesize: Optional[HumanFileSize] = DEFAULT_MAX_FILESIZE
    cache: Path = DEFAULT_CACHE_PATH
    mmess_path: Path = DEFAULT_MMESS_PATH
    morlab_path: Path = DEFAULT_MORLAB_PATH
    tectonic_path: Path = DEFAULT_TECTONIC_PATH

    # Pydantic Model config: to import the settings from environment variables
    model_config = SettingsConfigDict(
        env_prefix="morbfetch_",
        extra="ignore",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """
        Customise the settings sources and priorities to include a YAML file and environment variable.

        Priority: Source file defaults < YAML File < Environment Variables
        """
        CONFIG_FILE = (
            Path(os.getenv("MORBFETCH_CONFIG_FILE", DEFAULT_CONFIG_FILE))
            .expanduser()
            .resolve(strict=False)
        )
        assert TypeAdapter(ConfigFilename).validate_python(str(CONFIG_FILE))

        # CONFIG_FILE specified, but check if exists
        if not CONFIG_FILE.exists():
            return (env_settings, init_settings)
        else:
            logger.info(f"[italic orange1]Config:[/italic orange1] {CONFIG_FILE}")
            return (
                env_settings,
                YamlConfigSettingsSource(settings_cls, yaml_file=CONFIG_FILE),
                init_settings,
            )


# Singleton pattern for global access
_config: Settings | None = None


def get_config() -> Settings:
    """
    Get the global configuration for package

    Returns:
        Settings: The global configuration settings.
    """
    global _config
    if _config is None:
        _config = Settings()

    return _config


def clear_config():
    """
    Unset the global configuration for package
    """
    global _config
    _config = None


def print_config() -> None:
    """
    Print the current configuration.
    """

    def _print_dict_as_table(
        title: str,
        data: dict,
        colors: Optional[list[str]] = None,
        console: Optional[Console] = None,
    ):
        if colors is None:
            colors = ["magenta", "deep_sky_blue1", "orange1"]
        if console is None:
            console = Console()

        table = Table(
            title=title,
            show_header=False,
            box=None,
            title_justify="left",
            title_style=f"{colors[2]}",
        )

        table.add_column(style=f"{colors[0]}")
        table.add_column(style=f"{colors[1]}")

        for key, value in data.items():
            table.add_row(str(key), str(value))

        return console.print(table)

    _print_dict_as_table(
        title="morb_fetch configuration:", data=get_config().model_dump(), console=Console()
    )


def create_config(yaml_path: Path):
    """
    Create a new configuration file at the specified path.

    Args:
        yaml_path (Path): The path to the YAML configuration file.
    """
    config_data = (
        "# Server configuration for MORB-Fetch\n"
        "# Server URL, database file and file hash\n"
        f'serverurl: "{DEFAULT_SERVER_URL}"\n'
        f'indexfile: "{DEFAULT_INDEXFILE}"\n'
        f'indexfilehash: "{DEFAULT_INDEXFILEHASH}"\n'
        '# Restrict downloads to file size\n'
        f'max_filesize: "{DEFAULT_MAX_FILESIZE}"\n'
        "# Custom Cache location\n"
        f'cache: "{str(DEFAULT_CACHE_PATH)}"\n'
        "# Custom MESS location\n"
        f'mmess_path: "{str(DEFAULT_MMESS_PATH)}"\n'
        "# Custom MORLAB location\n"
        f'morlab_path: "{str(DEFAULT_MORLAB_PATH)}"\n'
        "# Custom TECTONIC location\n"
        f'tectonic_path: "{str(DEFAULT_TECTONIC_PATH)}"\n'
    )

    if yaml_path.exists():
        print("Config already exists!")
    else:
        with open(yaml_path, "w") as f:
            f.write(config_data)


def list_config():
    """
    List available configuration files in the current working directory,
    user configuration directory and any context included due to environment variables.
    """
    yaml_file = "morb_fetch.config.yaml"

    # Find if yaml file found in env
    paths = [
        Path(os.getenv("MORBFETCH_CONFIG_FILE", DEFAULT_CONFIG_FILE))
        .expanduser()
        .resolve(strict=False),
        Path.cwd() / yaml_file,
        user_config_path(appname="morb", appauthor="morb-users") / yaml_file,
    ]

    existing_configs = [path for path in set(paths) if path.exists()]

    if existing_configs:
        print("Found configs at:")
        for config in existing_configs:
            print(f" - {config}")
    else:
        print("No configs found!")

    return existing_configs


def delete_config(yaml_path: Path):
    """
    Delete a YAML configuration file.

    Args:
        yaml_path (Path): Path to the YAML configuration file.
    """
    if yaml_path.exists():
        yaml_path.unlink()
        print(f"Deleted config at {yaml_path}")
    else:
        print(f"Config not found at {yaml_path}")
