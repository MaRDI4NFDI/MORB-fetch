from morb_fetch.toolkits.toolkit import ZenodoToolkitDownloader
from morb_fetch.config import get_config


class MORLABDownloader(ZenodoToolkitDownloader):
    name = "morlab"
    registry = {
        "6.0": "doi:10.5281/zenodo.7072831",
        "5.0": "doi:10.5281/zenodo.3332716",
        "4.0": "doi:10.5281/zenodo.1574083",
        "3.0": "doi:10.5281/zenodo.842659",
    }
    download_path = get_config().morlab_path
