from morb_fetch.toolkits.toolkit import ZenodoToolkitDownloader
from morb_fetch.config import get_config


class MMESSDownloader(ZenodoToolkitDownloader):
    name = "MMESS"
    registry = {
        "3.1": "doi:10.5281/zenodo.14929081",
        "3.0": "doi:10.5281/zenodo.7701424",
        "2.2": "doi:10.5281/zenodo.5938237",
        "2.1": "doi:10.5281/zenodo.4719688",
        "2.0.1": "doi:10.5281/zenodo.3606345",
        "2.0": "doi:10.5281/zenodo.3368844",
        "1.0.1": "doi:10.5281/zenodo.50575",
    }
    download_path = get_config().mmess_path
