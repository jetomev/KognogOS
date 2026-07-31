import QtQuick 2.5

// KognogOS KSplash — matches the Plymouth theme: Mocha base, the tier
// emblem centered, a mauve ring spinning below. Shown from SDDM handoff
// until the Plasma session is ready.
Rectangle {
    id: root
    color: "#1e1e2e"
    property int stage

    Image {
        id: logo
        source: "file:///usr/share/pixmaps/kognogos.png"
        width: 220; height: 220
        anchors.centerIn: parent
        anchors.verticalCenterOffset: -40
        smooth: false   // keep the pixel-art edge
    }

    Image {
        id: spinner
        source: "file:///usr/share/pixmaps/kognogos-spinner.png"
        width: 48; height: 48
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: logo.bottom
        anchors.topMargin: 28
        RotationAnimation on rotation {
            from: 0; to: -360
            duration: 1500
            loops: Animation.Infinite
        }
    }
}
