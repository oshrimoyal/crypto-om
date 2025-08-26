import os
import yaml
from functools import lru_cache
from typing import Any


CONFIG_PATH = os.getenv("CONFIG_PATH", "configs/default.yaml")


@lru_cache(maxsize=None)
def _load_config() -> dict:
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def get_param(path: str, default: Any = None) -> Any:
    """
    Retrieve a configuration parameter by dotted path.  Returns `default` if missing.
    """
    parts = path.split(".")
    cfg = _load_config()
    for p in parts:
        if isinstance(cfg, dict) and p in cfg:
            cfg = cfg[p]
        else:
            return default
    return cfg