# Installation

This guide provides instructions for installing the `morb-fetch` package. As the project is not yet available on PyPI, it must be installed directly from its Git repository.

## Prerequisites

- **Python** (3.10 or newer is recommended)
- **pip** (the Python package installer)

We strongly recommend installing `morb-fetch` within a **virtual environment** to avoid conflicts with other packages on your system.

## Standard Installation with pip

This is the recommended method for most users.

1.  **Create and activate a virtual environment:**
    ```bash
    # Create the environment
    python3 -m venv .venv

    # Activate it (on macOS/Linux)
    source .venv/bin/activate

    # Or on Windows (PowerShell)
    .venv\Scripts\Activate.ps1
    ```

2.  **Install the package using pip:**
    ```bash
    pip install git+https://github.com/mardi4nfdi/morb-fetch.git
    ```

## Alternative: Installation with uv

If you use [`uv`](https://astral.sh/uv), you can use it for installation.

-   **To simply install `morb-fetch`** in the current environment (the equivalent of the `pip` command above):
    ```bash
    uv pip install git+https://github.com/mardi4nfdi/morb-fetch.git
    ```

-   **To add `morb-fetch` as a dependency to your own project's `pyproject.toml`** and install it:
    ```bash
    uv add git+https://github.com/mardi4nfdi/morb-fetch.git
    ```

## Verifying the Installation

To confirm that `morb-fetch` was installed correctly, you can run the following command. It should print the active configuration without any errors.

```bash
python3 -m morb_fetch --print-config
```

## Quickstart: Basic Usage

Once installed, you can import and use `morb_fetch` in your Python scripts. Here is a basic example of how to query the database and retrieve an *example*.

```python
from morb_fetch import Database, Example

# Initialize the database, which fetches the index of examples
database = Database()

# List all available example identifiers
print("Available IDs:", database.list_ids())

# Select an ID and create an Example instance
example_id = "steelProfile_n1357m7q6"
example = Example(example_id, database)

# Access the example's metadata
# This is equivalent to database.lookup(id)
metadata = example.meta
print("Metadata:", metadata)

# Fetch the system matrices from the remote server
example.retrieve()
matrices = example.data
print("Loaded matrices:", matrices.keys())
```

:::{note[Package Naming Convention]}
The installable package name uses a hyphen (`morb-fetch`), but the importable Python module uses an underscore (`morb_fetch`).
This is a common convention in the Python ecosystem.
:::

## Next Steps

-   **Explore Demos:** The `demos/` directory in the repository contains executable scripts that showcase usage. For example:
    ```bash
    # (After cloning the repository)
    python3 demos/plate.py
    ```

-   **Customize Behavior:** `morb-fetch` supports flexible configuration via environment variables or a YAML file. See the {ref}`Configuration Guide <id-configuration>` to learn more.

-   **Contribute to the Project:** For instructions on setting up a development environment, running tests, and building documentation, please refer to the {ref}`Developer Guide <id-dev-notes>`.
