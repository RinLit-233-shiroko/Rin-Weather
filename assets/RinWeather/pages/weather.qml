import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import Qt5Compat.GraphicalEffects  // 图形库
import RinUI
import RinWeather  // 导入自定义组件

FluentPage {
    id: weatherPage

    wrapperWidth: 800
    padding: 12

    Connections {
        id: updateConnection
        target: WeatherManager
        onWeatherUpdated: {
            updateWeather()
            weatherPage.loading = false
            footerText.lastUpdatedDate = WeatherManager.getLastUpdateTime()

            console.log("Weather updated")
        }
    }

    property var currentAQI: []
    property var currentUVI: 0
    property var currentWeather: {}
    property var currentTemperatures: []
    property var hourlyForecast: []
    property var dailyForecast: []
    property bool loading: true

    function updateWeather() {
        currentAQI = WeatherManager.getCurrentAQI()
        currentUVI = WeatherManager.getCurrentUVI()
        currentWeather = WeatherManager.getCurrentWeather()
        currentTemperatures = WeatherManager.getCurrentTemperatures()
        hourlyForecast = WeatherManager.getHoursForecast()
        dailyForecast = WeatherManager.getDaysForecast()
    }

    header: ColumnLayout {
        id: customHeader
        spacing: 8
        width: parent.width

        Image {
            height: 16
        }

        // 当前城市
        Text {
            typography: Typography.BodyLarge
            Layout.alignment: Qt.AlignHCenter
            color: "white"
            text: currentWeather["city"]
        }

        // 当前温度
        Text {
            typography: Typography.Display
            Layout.alignment: Qt.AlignHCenter
            color: "white"
            text: {
                let result = Math.round(currentWeather["temperature"]) + "°"
                return result
            }
        }

        RowLayout {
            spacing: 6
            Layout.alignment: Qt.AlignHCenter

            Image {
                Layout.alignment: Qt.AlignVCenter
                Layout.preferredWidth: 28
                Layout.preferredHeight: 28
                source: WeatherResource.getWeatherImage(currentWeather["weathercode"])
                fillMode: Image.PreserveAspectFit
            }
            Text {
                Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
                typography: Typography.BodyStrong
                color: "white"
                opacity: 0.6
                text: WeatherResource.getWeatherDescription(currentWeather["weathercode"])
            }
        }
        Text {
            typography: Typography.BodyStrong
            color: "white"
            Layout.alignment: Qt.AlignHCenter
            text: qsTr("H:" + currentTemperatures[0] + "° L:" + currentTemperatures[1] + "°")
            visible: !loading
        }

        Image {
            height: 16
        }
    }

    background: DynamicBackground {
        id: bg
        anchors.fill: parent
    }

    Slider {
        id: hourSlider
        Layout.preferredWidth: 300
        from: 0
        to: 23.99
        stepSize: 0.01
        value: 0
        onValueChanged: {
            bg.currentHour = value
        }
    }


    GridLayout {
        id: grid
        Layout.fillWidth: true
        columns: 2
        rowSpacing: 8
        columnSpacing: 8
        layoutDirection: GridLayout.LeftToRight

        // 每块都是一个小卡片组件
        WeatherClip {
            Layout.columnSpan: 2
            icon.name: "ic_fluent_clock_20_regular"
            text: qsTr("HOURLY FORECAST")
            ForecastModel {
                anchors.fill: parent
                model: hourlyForecast
            }
        }

        WeatherClip {
            Layout.columnSpan: 2
            Layout.preferredHeight: 300
            icon.name: "ic_fluent_calendar_20_regular"
            text: qsTr("7-DAY FORECAST")
            ForecastModelExpanded {
                anchors.fill: parent
                model: dailyForecast
            }
        }

        WeatherClip {
            text: qsTr("AIR QUALITY")
            icon.name: "ic_fluent_grid_dots_20_regular"
            AQI_Model {
                anchors.fill: parent
                aqi: currentAQI
            }
            onClicked: {
                aqiDialog.open()
            }

            AQI_Dialog {
                id: aqiDialog
                aqi: currentAQI
                width: Math.max(weatherPage.width * 0.4, 350)
                height: Math.min(weatherPage.height * 0.8, aqiDialog.implicitHeight)
            }
        }

        WeatherClip {
            text: qsTr("UV INDEX")
            icon.name: "ic_fluent_weather_sunny_20_filled"
            UVI_Model {
                anchors.fill: parent
                uvi: currentUVI
            }
            onClicked: {
                uviDialog.open()
            }

            UVI_Dialog {
                id: uviDialog
                uvi: currentUVI
                width: Math.max(weatherPage.width * 0.4, 350)
                height: Math.min(weatherPage.height * 0.8, uviDialog.implicitHeight)
            }
        }

        WeatherClip {
            text: qsTr("PRECIPITATION")
            icon.name: "ic_fluent_weather_blowing_snow_20_regular"
            // contentItem: TemperatureChart {}
        }

        WeatherClip {
            text: qsTr("WIND")
            icon.name: "ic_fluent_weather_blowing_snow_20_regular"
            // contentItem: TemperatureChart {}
        }

        WeatherClip {
            text: qsTr("FEELS LIKE")
            icon.name: "ic_fluent_temperature_20_regular"
            // contentItem: TemperatureChart {}
        }
    }

    Text {
        id: footerText
        Layout.alignment: Qt.AlignHCenter
        horizontalAlignment : Text.AlignHCenter
        typography: Typography.Caption
        color: Colors.proxy.textSecondaryColor
        property var lastUpdatedDate: "1970-01-01 00:00:00"

        text: qsTr("Last Updated: " + lastUpdatedDate + "<br> Weather data provided by <b>Open Meteo</b>")
    }
}