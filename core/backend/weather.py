import json
import requests
from typing import Optional, Dict, Any
from core import rw_config, DEFAULT_CONFIG
import core.backend.parser as parser
from loguru import logger
from datetime import datetime

from PySide6.QtCore import QObject, Slot, QDateTime, QTimer, Signal, QThread


proxies = {
    "http": None,
    "https": None
}


class WeatherRequester:
    def __init__(self, location: Optional[Dict[str, Any]] = None, config: Optional[Dict[str, Any]] = None):
        super().__init__()
        self.config = config or rw_config or DEFAULT_CONFIG

        if not location:
            self.city_config = {
                "city_name": self.config["weather"]["cities"][0]["name"],
                "latitude": self.config["weather"]["cities"][0]["latitude"],
                "longitude": self.config["weather"]["cities"][0]["longitude"]
            }
        else:
            self.city_config = location

        self.temp_unit = self.config["weather"]["temp_unit"]  # 单位
        self.windspeed_unit = self.config["weather"]["windspeed_unit"]
        self.precipitation_unit = self.config["weather"]["precipitation_unit"]

        self.base_url = "https://api.open-meteo.com/v1/forecast"
        self.aqi_url = "https://air-quality-api.open-meteo.com/v1/air-quality"
        self.result = {}
        self.date = None

    def fetch_weather(self) -> Optional[Dict[str, Any]]:
        params = {
            "latitude": self.city_config["latitude"],  # 纬度
            "longitude": self.city_config["longitude"], "current_weather": True,  # 经度
            "temperature_unit": self.temp_unit,  # or "fahrenheit"
            "windspeed_unit": self.windspeed_unit,  # or "kmh", "mph", "kn"
            "precipitation_unit": self.precipitation_unit,  # or "inch"
            "timezone": "auto",
            "hourly": ",".join([
                "temperature_2m", "weathercode", "precipitation",
                "cloudcover", "windspeed_10m", "apparent_temperature",
                "uv_index"
            ]),
            "forecast_days": 7,
            "daily": ",".join([
                "temperature_2m_max", "temperature_2m_min", "weathercode",
                "precipitation_sum", "sunrise", "sunset"  # 日升日落时间
            ])

        }

        aqi_params = {
            "latitude": self.city_config["latitude"],
            "longitude": self.city_config["longitude"],
            "hourly": "european_aqi",
            "timezone": "auto"
        }

        try:
            logger.info("正在请求天气数据…")
            res = requests.get(self.base_url, params=params, timeout=5, proxies=proxies)
            aqi_res = requests.get(self.aqi_url, params=aqi_params, timeout=5, proxies=proxies)
            print("请求URL:", res.url)
            print("AQI请求URL:", aqi_res.url)
            res.raise_for_status()
            aqi_res.raise_for_status()
            return self.parse_weather(res.json(), aqi_res.json())
        except requests.exceptions.Timeout:
            logger.error("请求超时，请检查网络连接")
            return None
        except requests.RequestException as e:
            logger.error(f"请求失败：{e}")
            return None

    def parse_weather(self, data: Dict[str, Any], aqi_data: Dict[str, Any]) -> Dict[str, Any]:
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info("已获取")
        aqi = aqi_data["hourly"].get("european_aqi", [])
        data["aqi"] = aqi
        return data


class WeatherManager(QObject):
    weatherUpdated = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.requester = WeatherRequester()
        self.weather_data = None

        # 定时刷新
        self.timer = QTimer(self)
        self.timer.setInterval(60 * 60 * 1000)  # 每小时更新一次
        self.timer.timeout.connect(self.refreshWeather)
        self.timer.start()

        self.refreshWeather()

    @Slot()
    def refreshWeather(self):
        self.thread = QThread()
        self.worker = WeatherWorker(self.requester)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self._onWeatherDataReceived)
        self.worker.error.connect(self._onWeatherError)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def _onWeatherDataReceived(self, data):
        self.weather_data = data
        self.weatherUpdated.emit()
        logger.info(f"天气数据更新于 {self.requester.date}")

    def _onWeatherError(self, error):
        logger.warning(f"天气获取失败：{error}")

    @Slot(result=str)
    def getCity(self):
        return self.requester.city_config["city_name"] or "Unknown"

    @Slot(result=dict)
    def getCurrentWeather(self):
        result = self.weather_data.get("current_weather") if self.weather_data else {}
        result["city"] = self.getCity()
        return result

    @Slot(result=list)
    def getCurrentTemperatures(self) -> list:
        result = self.weather_data.get("daily") if self.weather_data else []
        h_temp = int(result.get("temperature_2m_max")[0])
        l_temp = int(result.get("temperature_2m_min")[0])
        return [h_temp, l_temp]

    @Slot(result=int)
    def getCurrentAQI(self) -> int:
        return parser.get_current_aqi(self.weather_data.get("hourly"), self.weather_data.get("aqi")) if\
            self.weather_data else 0

    @Slot(result=int)
    def getCurrentUVI(self):
        return parser.get_current_uvi(self.weather_data.get("hourly")) if self.weather_data else 0

    @Slot(result=list)
    def getHoursForecast(self):
        return parser.parse_hourly_data(self.weather_data.get("hourly")) if self.weather_data else []

    @Slot(result=list)
    def getDaysForecast(self):
        return parser.parse_daily_data(self.weather_data.get("daily")) if self.weather_data else []

    @Slot(result=str)
    def getLastUpdateTime(self):
        return self.requester.date or QDateTime.currentDateTime().toString()


class WeatherWorker(QObject):
    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, requester):
        super().__init__()
        self.requester = requester

    def run(self):
        try:
            result = self.requester.fetch_weather()
            if result:
                self.finished.emit(result)
            else:
                self.error.emit("返回为空")
        except Exception as e:
            self.error.emit(str(e))


if __name__ == "__main__":
    center = WeatherRequester()
    print(center.fetch_weather())
