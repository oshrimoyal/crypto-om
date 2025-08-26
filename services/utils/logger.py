import logging
import logging.config
import yaml
from pathlib import Path


def setup_logging(config_path: str = "configs/logging.yaml") -> None:
    """
    Configure the logging module using a YAML configuration file.
    """
    if Path(config_path).exists():
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=logging.INFO)


setup_logging()
logger = logging.getLogger("services")