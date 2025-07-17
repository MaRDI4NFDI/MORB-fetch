# MORB-fetch

A configurable data (and metadata) fetcher for datasets and toolkits used in Model Order Reduction Benchmarker (MORB).

Features:
- Easy dataset selection, download, extraction
- Downloaders for MORLAB, M-MESS and Tectonic toolkits
- Flexible configuration options and dataset-caching
- Strict type checking
- Integration with MORB for seamless benchmarking

Authors:
- Ashwin S. Nayak
  [![orcid](https://img.shields.io/badge/%20-orcid-black?logo=orcid&style=plastic)](https://orcid.org/0000-0002-9855-2377)
  [![github](https://img.shields.io/badge/%20-github-black?logo=github&style=plastic)](https://github.com/ashwin-nayak)
- Jens Saak
  [![orcid](https://img.shields.io/badge/%20-orcid-black?logo=orcid&style=plastic)](https://orcid.org/0000-0001-5567-9637)
  [![github](https://img.shields.io/badge/%20-github-black?logo=github&style=plastic)](https://github.com/drittelhacker)

Affiliation:
- [Max Planck Institute for Dynamics of Complex Technical Systems](https://www.mpi-magdeburg.mpg.de), Magdeburg, Germany.

License:
- BSD 3-Clause, see [`LICENSE`](LICENSE).

Documentation:
[![Documentation Status](https://readthedocs.org/projects/morb-fetch/badge/?version=latest)](https://morb-fetch.readthedocs.io/en/latest/?badge=latest)

## Installation

This project relies heavily on `uv`, a fast and efficient tool for managing Python projects and their dependencies. While this is not strictly necessary, it eases the installation process.

> [!tip]
> To install `uv`, check out the [official installation instructions](https://docs.astral.sh/uv/getting-started/installation/) for your platform. Alternatively, you can also install it via `pip`, `pipx`, `brew`, and by downloading the standalone binary.

The following sections provide more details on how to use this project for different purposes.

> [!note]
> For developers (testing, documentation and building), refer to [README.dev.md](README.dev.md).

### Use in your own projects

The project is yet to be published on PyPI, so to install this project as a dependency,

```bash
uv add git+https://github.com/mardi4nfdi/morb-fetch.git
```
> If using `pip`, you can install it via,
> ```
> pip install git+https://github.com/mardi4nfdi/morb-fetch.git
> ```

You can then use it in your code,
```python
from morb_fetch import Database, Example

# List all example identifiers in Database
database = Database()
ids = database.list_ids()

# Pull metadata using ID
id = "steelProfile_n1357m7q6"
example = Example(id, database)
metadata = example.meta # or also, database.lookup(id)

# Fetch system matrices from Zenodo or server
example.retrieve()
matrices = example.data
```

The database currently has a subset of benchmarks in [MORWiki](https://modelreduction.org/morwiki), and it is best to list ids to check if they exist.

`MORB-Fetch` supports flexible configuration through environment variables or a YAML configuration file.

### Run Demos
First clone the repository,

```bash
git clone https://github.com/mardi4nfdi/morb-fetch.git
cd morb-fetch
```

Install the required dependencies,

```bash
uv sync
```
This command reads the dependencies from `pyproject.toml` and installs them into a virtual environment, which is created by default in the `.venv` directory.

Subsequently, you can run the demos,

```bash
uv run demos/steel_profile.py
```
