from typing import Optional, Dict, Any
from pathlib import Path
import requests
from assets import ROOT_PATH
from RinUI import ConfigManager


DEFAULT_CONFIG = {
    "weather": {
        "API_KEY": "",
        "temp_unit": "celsius",
        "windspeed_unit": "ms",               # or "kmh", "mph", "kn"
        "precipitation_unit": "mm",

        "cities": [
            {
                "name": "Beijing",
                "latitude": 39.9042,
                "longitude": 116.4074,
            }
        ]
    }
}


class WeatherConfig(ConfigManager):
    def __init__(self):
        path = ROOT_PATH
        filename = "config.json"
        super().__init__(path, filename)

        self.load_config(DEFAULT_CONFIG)


rw_config = None
