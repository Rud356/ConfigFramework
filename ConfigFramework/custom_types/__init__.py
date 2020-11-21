import logging
from ConfigFramework.settings import config

logger = logging.Logger("ConfigFramework logger", level=logging.WARN)
logger.addHandler(logging.FileHandler(
    config.get("LoadersVariables", "LogPath", fallback='ConfigFramework.log'), 'a', 'utf8'
))
logger.addHandler(logging.Handler(level=logging.WARN))

from .config_variable import *
from .loaders import *
