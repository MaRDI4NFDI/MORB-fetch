(id-configuration)=
# Configuration

`morb-fetch` offers a flexible configuration system that allows you to customize its behavior. Settings can be specified through environment variables or a YAML configuration file.

The precedence for configuration values is as follows, with higher-listed sources overriding lower ones:

1.  **Environment Variables**: Highest priority.
2.  **Configuration File (YAML)**: Overridden by environment variables.
3.  **Default Configuration**: Lowest priority.

### Inspecting the Active Configuration

To see the final configuration that `morb-fetch` is using after applying all overrides, you can print it to the console. This is useful for debugging your setup.

From the command line:
```bash
python3 -m morb_fetch --print-config
```

Or from within a Python script:
```python
from morb_fetch import print_config

print_config()
```

## Configuration Properties

The following sections detail each configurable property, including its default value and how to override it using either an environment variable or a YAML configuration file key.

### Server URL

The base URL of the server where example data is hosted.

- **Default**: `https://modelreduction.org/morb-data/`
- **Environment Variable**: `MORBFETCH_SERVERURL`
- **YAML Key**: `serverurl`

### Index File

The name of the CSV file that contains the list of available MORWiki examples with their metadata.
Additionally the tool looks for this indexfile at Server URL to fetch list of available examples.

- **Default**: `examples.csv`
- **Environment Variable**: `MORBFETCH_INDEXFILE`
- **YAML Key**: `indexfile`

### Index File Hash

The expected SHA256 hash of the index file, used to verify its integrity.

- **Default**: `sha256:<hash>`
- **Environment Variable**: `MORBFETCH_INDEXFILEHASH`
- **YAML Key**: `indexfile_hash`

### Maximum File Size

A limit on the size of files that can be downloaded. Values can be specified with units (e.g., `100MB`, `1.5 GiB`).

- **Default**: `None` (no limit)
- **Environment Variable**: `MORBFETCH_MAX_FILESIZE`
- **YAML Key**: `max_filesize`

Example: To set a 100MB limit via an environment variable:
```bash
export MORBFETCH_MAX_FILESIZE=100MB
```

### Cache Location

The primary directory where downloaded files and the index are stored.
The examples and their datasets will be located within `<cache_location>/data/`.

- **Default**: A platform-specific cache directory (e.g., `~/.cache/morb` on Linux).
- **Environment Variable**: `MORBFETCH_CACHE`
- **YAML Key**: `cache`

### MMESS Download Path

The specific subdirectory for storing MMESS.
MMESS is downloaded as a zip file from it's [Zenodo registry](https://zenodo.org/records/14929081) and unzipped into this directory.
The zip file is kept in the same directory for future reference.

- **Default**: A folder named `MMESS` inside the cache location (e.g., `~/.cache/morb/MMESS`).
- **Environment Variable**: `MORBFETCH_MMESS_PATH`
- **YAML Key**: `mmess_path`

### MORLAB Download Path

The specific subdirectory for storing MORLAB.
MORLAB is downloaded as a zip file from it's [Zenodo registry](https://zenodo.org/records/7072831) and unzipped into this directory.
The zip file is kept in the same directory for future reference.

- **Default**: A folder named `morlab` inside the cache location (e.g., `~/.cache/morb/morlab`).
- **Environment Variable**: `MORBFETCH_MORLAB_PATH`
- **YAML Key**: `morlab_path`

### TECTONIC Download Path

The specific subdirectory for storing [TECTONIC](https://tectonic-typesetting.github.io) binaries.
TECTONIC is downloaded as a `tar.gz` file (for Unix and Mac-OS) or a `zip` file (for Windows) from it's [Github Releases](https://github.com/tectonic-typesetting/tectonic/releases) page and unzipped into this directory.
The compressed file is kept in the same directory for future reference.

- **Default**: A folder named `tectonic` inside the Cache Location (e.g., `~/.cache/morb/tectonic`).
- **Environment Variable**: `MORBFETCH_TECTONIC_PATH`
- **YAML Key**: `tectonic_path`

## Using a Configuration File

Using environment variables can be inconvenient for complex setups or when you want to share configurations across multiple users or machines.
A configuration file provides a more structured and flexible way to manage settings and MORB lets you define your settings in a YAML file named `morb_fetch.config.yaml`.

### File Location and Precedence

`morb-fetch` searches for the configuration file in the following locations, in order:

1.  The path specified by the `MORBFETCH_CONFIG_FILE` environment variable.
2.  `morb_fetch.config.yaml` in the current working directory.
3.  `morb_fetch.config.yaml` in the user's application configuration directory (e.g., `~/.config/morb/` on Linux).

To use a configuration file from a custom location (or a different file name), set the environment variable:
```bash
export MORBFETCH_CONFIG_FILE=/path/to/my_custom_config.yaml
```

### Creating and Using a Configuration File

You can generate a template configuration file. If a path is provided, the file is created there; otherwise, it is created in the current directory.

```bash
# Create a config file in /etc/morb_fetch/
python3 -m morb_fetch --create-config /etc/morb_fetch/

# Create a config file in the user's config directory
python3 -m morb_fetch --create-config user
```

A complete `morb_fetch.config.yaml` file looks like this:

```yaml
# The base URL for the server.
serverurl: "https://modelreduction.org/morb-data/"

# The filename of the index file.
indexfile: "examples.csv"

# The SHA256 hash of the index file for verification.
indexfilehash: "sha256:6511ed223cce32e501c486fbfb0fa30453486366b56d1d1f1b8367f09272c9bb"

# The maximum file size allowed for download (e.g., "500MB", "2GB"). Set to "None" for no limit.
max_filesize: "None"

# The path to the main cache directory.
cache: "~/.cache/morb"

# The path to the MMESS download directory (absolute path).
mmess_path: "/path/to/MMESS"

# The path to the MORLAB download directory (absolute path).
morlab_path: "/path/to/morlab"

# The path to the TECTONIC download directory (absolute path).
tectonic_path: "/path/to/tectonic"
```

### Managing Configuration Files

`morb-fetch` provides command-line tools to help manage your configuration files.

**List Discovered Files**

To see which configuration files `morb-fetch` finds based on its search precedence:
```bash
python3 -m morb_fetch --list-config
```

**Delete Configuration Files**

To delete a specific configuration file (OS-independent):
```bash
python3 -m morb_fetch --delete-config /path/to/morb_fetch.config.yaml
```

To delete all configuration files found by `morb-fetch`:
```bash
python3 -m morb_fetch --delete-config all
```

:::{note}
These management functions are ideal for handling the static configuration of `morb_fetch`.
If you are modifying configuration dynamically within an application, you may need to call `clear_config()` before reloading the configuration with `get_config()` to ensure changes are applied.
:::
