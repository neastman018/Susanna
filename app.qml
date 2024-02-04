import QtQuick
import QtQuick.Controls.Basic
ApplicationWindow {
    visible: true
    width: screen.desktopAvailableWidth
    height: screen.desktopAvailableHeight
    x: screen.desktopAvailableWidth - width
    y: screen.desktopAvailableHeight - height 
    flags: Qt.FramelessWindowHint | Qt.Window
    title: "HelloApp"

    property string currTime: "00:00:00"
    property QtObject backend


    Text {
        anchors.centerIn: parent
        text: currTime
        font.pixelSize: 24
    }

    Connections {
        target: backend
        function onUpdated(msg) {
            currTime = msg;
        }
    }
}