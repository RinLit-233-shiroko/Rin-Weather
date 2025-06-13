from datetime import datetime, timedelta, timezone, tzinfo
import platform
import re


def parse_timezone_abbr(tz_abbr: str) -> timezone | tzinfo | None:
    """
    简单解析类似 GMT+8 的时区缩写，返回对应 timezone 对象
    不支持复杂时区名称，只针对 GMT±数字 格式
    """
    match = re.match(r"GMT([+-])(\d+)", tz_abbr)
    if match:
        sign, hours = match.groups()
        offset_hours = int(hours)
        if sign == '-':
            offset_hours = -offset_hours
        return timezone(timedelta(hours=offset_hours))
    # 默认返回本地时区（无偏移）
    return datetime.now().astimezone().tzinfo


def parse_hourly_data(hourly: dict, units: dict = None, timezone_abbreviation: str = None) -> list:
    if units is None:
        units = {
            "temperature_2m": "°C",
            "precipitation": "mm",
            "cloudcover": "%",
            "windspeed_10m": "m/s",
            "apparent_temperature": "°C"
        }

    # 解析时区
    tz = parse_timezone_abbr(timezone_abbreviation) if timezone_abbreviation else datetime.now().astimezone().tzinfo

    result = []

    # 当前本地整点时间，带时区
    now = datetime.now(tz).replace(minute=0, second=0, microsecond=0)

    time_format = "%#I %p" if platform.system() == "Windows" else "%-I %p"

    entries = []
    for i in range(min(len(hourly["time"]), 48)):
        # 转为带 UTC 时区的 datetime 对象
        utc_time = datetime.strptime(hourly["time"][i], "%Y-%m-%dT%H:%M").replace(tzinfo=timezone.utc)
        # 转成本地时间，带解析的时区 tz
        local_time = utc_time.astimezone(tz)

        entries.append({
            "time_obj": local_time,
            "code": hourly["weathercode"][i],
            "temperature": round(hourly["temperature_2m"][i]),
            "precipitation": round(hourly.get("precipitation", [0])[i], 1)
        })

    # 过滤未来24小时，从当前时间开始（时区已正确）
    filtered = [entry for entry in entries if entry["time_obj"] >= now][:24]

    for entry in filtered:
        t = entry["time_obj"]
        is_now = t == now
        hour_label = "<b>Now</b>" if is_now else t.strftime(time_format)

        precip_val = entry["precipitation"]
        precip_str = None if precip_val == 0 else f"{precip_val}{units.get('precipitation', '')}"  # 降水

        result.append({
            "time": hour_label,
            "code": entry["code"],
            "temperature": f"{entry['temperature']}",  # 单位 {units.get('temperature_2m', '')}
            "precipitation": f"{precip_str}"
        })

    return result


def get_current_aqi(hourly: dict, aqis: dict, timezone_abbreviation: str = None) -> float:
    """
    从 hourly 数据中获取当前本地小时的 AQI 值
    """
    # 解析时区
    tz = parse_timezone_abbr(timezone_abbreviation) if timezone_abbreviation else datetime.now().astimezone().tzinfo

    now_local = datetime.now(tz).replace(minute=0, second=0, microsecond=0)
    now_str = now_local.strftime("%Y-%m-%dT%H:%M")

    try:
        index = hourly["time"].index(now_str)
        aqi = aqis[index]
        return round(aqi, 1)
    except (ValueError, KeyError, IndexError):
        return -1  # 未找到对应时间


def get_current_uvi(hourly: dict, timezone_abbreviation: str = None) -> float:
    """
    从 hourly 数据中获取当前本地小时的 UVI 值
    """
    # 解析时区
    tz = parse_timezone_abbr(timezone_abbreviation) if timezone_abbreviation else datetime.now().astimezone().tzinfo

    now_local = datetime.now(tz).replace(minute=0, second=0, microsecond=0)
    now_str = now_local.strftime("%Y-%m-%dT%H:%M")

    try:
        index = hourly["time"].index(now_str)
        uvi = hourly["uv_index"][index]
        return round(uvi, 1)
    except (ValueError, KeyError, IndexError):
        return -1  # 未找到对应时间


def parse_daily_data(daily: dict, units: dict = None) -> list:
    result = []

    if units is None:
        units = {
            "temperature_2m_max": "°C",
            "temperature_2m_min": "°C",
            "precipitation_sum": "mm",
        }

    for i in range(len(daily["time"])):
        date_str = daily["time"][i]
        code = daily["weathercode"][i]
        h_temp = round(daily["temperature_2m_max"][i])
        l_temp = round(daily["temperature_2m_min"][i])
        precipitation = daily["precipitation_sum"][i]

        precipitation_str = None if precipitation == 0 \
            else f"{round(precipitation, 1)}{units.get('precipitation_sum', '')}"

        result.append({
            "time": datetime.strptime(date_str, "%Y-%m-%d").strftime("%A"),
            "code": code,
            "h_temp": f"{h_temp}",
            "l_temp": f"{l_temp}",
            "precipitation": precipitation_str
        })

    return result
