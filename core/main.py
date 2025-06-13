from pathlib import Path
from RinUI import RinUIWindow

from assets import ASSETS_PATH, QML_PATH
from core import PathManager, WeatherResourceManager
from core import WeatherManager


class RinWeatherMain(RinUIWindow):
    def __init__(self):
        super().__init__()
        self.pathManager = PathManager()
        self.weatherResourceManager = WeatherResourceManager()
        self.weatherManager = WeatherManager()

        self.engine.addImportPath(Path(ASSETS_PATH))
        self.engine.rootContext().setContextProperty("RinPath", self.pathManager)
        self.engine.rootContext().setContextProperty("WeatherManager", self.weatherManager)
        self.engine.rootContext().setContextProperty("WeatherResource", self.weatherResourceManager)

        print("🌦️ RinWeather Application Initialized")

        self.load(Path(QML_PATH, "app.qml"))



