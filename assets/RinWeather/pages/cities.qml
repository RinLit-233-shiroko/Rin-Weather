import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 2.15
import Qt5Compat.GraphicalEffects  // 图形库
import RinUI
import RinWeather  // 导入自定义组件

FluentPage {
    id: citiesPage

    header: Item {
        id: container
        height: headerRow.height + 44

        RowLayout {
            id: headerRow
            width: Math.min(citiesPage.width - citiesPage.horizontalPadding * 2, citiesPage.wrapperWidth)  // 限制最大宽度
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.bottomMargin: 12
            anchors.bottom: parent.bottom

            Text {
                height: parent.height
                Layout.alignment: Qt.AlignLeft | Qt.AlignBottom
                typography: Typography.Title
                text: qsTr("Cities")
            }

            Item {
                Layout.fillWidth: true
            }

            spacing: 4
            ToolButton {
                icon.name: "ic_fluent_add_20_regular"
                ToolTip {
                    delay: 500
                    text: qsTr("Add city")
                    visible: parent.hovered
                }
                onClicked: {
                    addCityDialog.open()
                }
            }
        }
    }

    property var cities: [ ]

    Component.onCompleted: {
        cities = WeatherConfig.getCities()
    }

    // City List //
    Grid {
        id: cityGrid
        Layout.fillWidth: true
        rowSpacing: 12
        columnSpacing: 12
        columns: Math.floor(width / (200 + 12)) || 1

        Repeater {
            id: cityListView
            model: cities
            delegate: CityClip {
                menuVisible: true

                // 点击
                onClicked: {
                    WeatherConfig.setCurrentCity(index)
                    WeatherManager.setLocation(
                        {
                            "latitude": latitude,
                            "longitude": longitude,
                            "name": name
                        }
                    )
                    navigationView.safePush(Qt.resolvedUrl("../pages/weather.qml"))
                }
            }
        }
    }


    // Add City / Dialog //
    AddCity_Dialog {
        id: addCityDialog
    }
}