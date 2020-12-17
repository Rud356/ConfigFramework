import logging
from sys import stderr
from ConfigFramework.settings import config

logger = logging.Logger("ConfigFramework logger", level=logging.WARN)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
file_handler = logging.FileHandler(
    config.get("LoadersVariables", "LogPath", fallback='ConfigFramework.log'), 'a', 'utf8'
)
stream_handler = logging.StreamHandler()

file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

from .config_variable import *
from .loaders import *
