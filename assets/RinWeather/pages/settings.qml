import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 2.15
import Qt5Compat.GraphicalEffects  // 图形库
import RinUI
import RinWeather  // 导入自定义组件

FluentPage {
    id: citiesPage

    title: qsTr("Settings")

    Column {
        Layout.fillWidth: true
        spacing: 3
        Text {
            typography: Typography.BodyStrong
            text: qsTr("About")
        }

        SettingExpander {
            width: parent.width
            title: qsTr("Rin Weather")
            description: qsTr("© 2025 RinLit. All rights reserved.")
            // source: Qt.resolvedUrl("../assets/BA_Pic_Shiroko-chibi.png")
            // iconSize: 28

            content: Text {
                color: Theme.currentTheme.colors.textSecondaryColor
                text: "0.0.1"
            }

            SettingItem {
                id: repo
                title: qsTr("To clone this repository")

                TextInput {
                    id: repoUrl
                    readOnly: true
                    text: "git clone https://github.com/RinLit-233-shiroko/Rin-UI.git"
                    wrapMode: TextInput.Wrap
                }
                ToolButton {
                    flat: true
                    icon.name: "ic_fluent_copy_20_regular"
                    onClicked: {
                        Backend.copyToClipboard(repoUrl.text)
                    }
                }
            }
            SettingItem {
                title: qsTr("File a bug or request new sample")

                Hyperlink {
                    text: qsTr("Create an issue on GitHub")
                    openUrl: "https://github.com/microsoft/WinUI-Gallery/issues/new/choose"
                }
            }
            SettingItem {
                Column {
                    Layout.fillWidth: true
                    Text {
                        text: qsTr("Dependencies & references")
                    }
                    Hyperlink {
                        text: qsTr("Qt & Qt Quick")
                        openUrl: "https://www.qt.io/"
                    }
                    Hyperlink {
                        text: qsTr("Fluent Design System")
                        openUrl: "https://fluent2.microsoft.design/"
                    }
                    Hyperlink {
                        text: qsTr("Fluent UI System Icons")
                        openUrl: "https://github.com/microsoft/fluentui-system-icons/"
                    }
                    Hyperlink {
                        text: qsTr("WinUI 3 Gallery")
                        openUrl: "https://github.com/microsoft/WinUI-Gallery"
                    }
                }
            }
            SettingItem {
                title: qsTr("License")
                description: qsTr("This project is licensed under the MIT license")

                Hyperlink {
                    text: qsTr("MIT License")
                    openUrl: "https://github.com/RinLit-233-shiroko/Rin-UI/blob/master/LICENSE"
                }
            }
        }
    }
}