from pathlib import Path

from morb_fetch._types import HumanFileSize

def loadmat(filepath: Path) -> dict:
    """
    Load a MATLAB file using pymatreader.read_mat.

    Args:
        filepath (str): The path to the MATLAB file.

    Returns:
        dict: The loaded MATLAB data.
    """
    from pymatreader import read_mat
    return read_mat(filepath)


def parse_human_size(s: HumanFileSize) -> int:
    """
    Parse a human-readable size string into an integer.

    Args:
        s (HumanFileSize): The human-readable size string.

    Returns:
        int: The parsed size in bytes.

    Raises:
        ValueError: If the size string is invalid.
    """
    units = {
        "B": 1,
        "KB": 10**3,
        "MB": 10**6,
        "GB": 10**9,
        "KIB": 2**10,
        "MIB": 2**20,
        "GIB": 2**30,
    }
    s = s.strip().upper().replace(" ", "")
    for unit in sorted(units.keys(), key=len, reverse=True):
        if s.endswith(unit):
            num = float(s[: -len(unit)])
            return int(num * units[unit])

    raise ValueError(f"Could not parse size: {s}")

def setup_logging():
    from rich.logging import RichHandler
    import logging

    logger = logging.getLogger("morb_fetch")
    logger.setLevel(logging.INFO)
    handler = RichHandler(
        markup=True,
        show_time=False,
        show_level=False,
        show_path=False,
    )
    formatter = logging.Formatter("[orange1]morb_fetch[/orange1]: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
