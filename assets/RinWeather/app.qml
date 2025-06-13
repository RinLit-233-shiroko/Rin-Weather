import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import RinUI


FluentWindow {
    id: root
    title: "Rin Weather"
    width: 900
    height: 600
    visible: true

    navigationItems: [
        {
            title: "Weather",
            icon: "ic_fluent_weather_rain_showers_day_20_regular",
            page: Qt.resolvedUrl("pages/weather.qml"),
        },
    ]

    // navigationView.navigationBar.collapsed = true
}