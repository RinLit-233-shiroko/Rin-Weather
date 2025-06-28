from pathlib import Path

from PySide6.QtCore import QCoreApplication
from RinUI import RinUIWindow

from assets import ASSETS_PATH, QML_PATH, RESOURCES_PATH
from core import PathManager, WeatherResourceManager, WeatherManager, WeatherConfig, CityManager


class RinWeatherMain(RinUIWindow):
    def __init__(self):
        super().__init__()
        self.pathManager = PathManager()
        self.weatherResourceManager = WeatherResourceManager()
        self.weatherConfig = WeatherConfig()
        self.weatherManager = WeatherManager(self.weatherConfig)
        self.cityManager = CityManager()

        self.engine.addImportPath(Path(ASSETS_PATH))
        self.engine.rootContext().setContextProperty("RinPath", self.pathManager)
        self.engine.rootContext().setContextProperty("WeatherManager", self.weatherManager)
        self.engine.rootContext().setContextProperty("CityManager", self.cityManager)
        self.engine.rootContext().setContextProperty("WeatherConfig", self.weatherConfig)
        self.engine.rootContext().setContextProperty("WeatherResource", self.weatherResourceManager)

        print("🌦️ RinWeather Application Initialized")

        self.load(Path(QML_PATH, "app.qml"))
        self.setIcon(str(Path(RESOURCES_PATH / "images" / "logo.png")))

        app_instance = QCoreApplication.instance()
        app_instance.aboutToQuit.connect(self.cleanup)

    def cleanup(self):
        print("RinWeather Application Cleanup")
        self.weatherManager.cleanup()
        self.cityManager.cleanup()
