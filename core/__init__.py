from PySide6.QtCore import QObject, Slot
from assets import ASSETS_PATH
from .backend.resources import WeatherResourceManager
from .backend.config import rw_config, WeatherConfig, DEFAULT_CONFIG
from .backend.weather import WeatherManager


class PathManager(QObject):

    @Slot(str, result=str)
    def assets(self, args: str) -> str:
        """
        Get the absolute path to an asset file within the assets' directory.
        :param args: Path components to append to the assets' directory.
        :return: Absolute path to the specified asset.
        """
        return ASSETS_PATH.joinpath(args).resolve().as_uri()
