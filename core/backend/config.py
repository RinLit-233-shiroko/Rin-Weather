from typing import Optional, Dict, Any
from pathlib import Path
import requests
from PySide6.QtCore import QObject, Slot, Signal
from loguru import logger

from assets import ROOT_PATH
from RinUI import ConfigManager


DEV_MODE = False
DEFAULT_CONFIG = {
    "weather": {
        "API_KEY": "",
        "temp_unit": "celsius",
        "windspeed_unit": "ms",               # or "kmh", "mph", "kn"
        "precipitation_unit": "mm",

        "current_city": 0,

        "cities": [
            {
                "name": "Beijing",
                "latitude": 39.9042,
                "longitude": 116.4074,
            },
            {
                "name": "Shanghai",
                "latitude": 31.2304,
                "longitude": 121.4737,
            }
        ]
    },
    "network": {
        "proxy": {
            "http": None,
            "https": None
        },
        "cache_expiration": 600,
    },
    "locale": {
        "language": "en_US",
    }
}


class WeatherConfig(ConfigManager, QObject):
    dataUpdated = Signal()

    def __init__(self):
        path = ROOT_PATH
        filename = "config.json"

        ConfigManager.__init__(self, path, filename)
        QObject.__init__(self)

        if DEV_MODE:
            self.config = DEFAULT_CONFIG
        else:
            self.load_config(DEFAULT_CONFIG)

    @Slot(result=list)
    def getCities(self) -> list:
        return self.config["weather"]["cities"]

    @Slot(str, float, float)
    def addCity(self, name: str, latitude: float, longitude: float) -> None:
        cities = self.config["weather"]["cities"]
        cities.append({
            "name": name,
            "latitude": latitude,
            "longitude": longitude,
        })
        self.dataUpdated.emit()
        self.save_config()

    @Slot(int)
    def removeCity(self, key: int) -> None:
        cities = self.config["weather"]["cities"]
        if len(cities) <= 1:
            logger.warning("Cannot remove the last city.")
            return

        cities.pop(key)
        self.dataUpdated.emit()
        self.save_config()

    @Slot(int)
    def setCurrentCity(self, index: int) -> None:
        if 0 <= index < len(self.config["weather"]["cities"]):
            self.config["weather"]["current_city"] = index
            self.dataUpdated.emit()
            self.save_config()
        else:
            raise IndexError("Index out of range for current city.")
