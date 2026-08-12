/*
    KognogOS Plasma splash.

    Deliberately the same picture as the Plymouth theme — same Mocha base,
    the same logo.png and spinner.png files, the same emblem-above-spinner
    layout — so the screen that appears after login reads as a continuation
    of the one that appeared before it rather than a second, different
    brand. The progress rule sweeps blue → ember, echoing the band across
    the GRUB background.

    SPDX-FileCopyrightText: 2026 Javier
    SPDX-License-Identifier: GPL-3.0-or-later
*/

import QtQuick
import org.kde.kirigami 2 as Kirigami

Rectangle {
    id: root

    // Catppuccin Mocha base — identical to Window.SetBackground*Color
    // in kognog.script, so the handoff has no visible seam.
    color: "#1e1e2e"

    property int stage

    // Plasma walks stages 1..6. Fade the content in early, then let the
    // rule track progress; at the last stage everything fades back out
    // so the desktop does not punch through a fully opaque splash.
    onStageChanged: {
        if (stage === 2) {
            contentFade.running = true;
        } else if (stage === 6) {
            outroFade.running = true;
        }
    }

    Item {
        id: content
        anchors.fill: parent
        opacity: 0

        Image {
            id: logo

            readonly property real size: Kirigami.Units.gridUnit * 10

            source: "images/logo.png"
            smooth: true
            sourceSize.width: size
            sourceSize.height: size

            anchors.horizontalCenter: parent.horizontalCenter
            // Mirrors Plymouth's `- 40` nudge above centre, expressed in
            // grid units so it survives HiDPI instead of drifting.
            y: (parent.height - height) / 2 - Kirigami.Units.gridUnit * 2.5
        }

        Text {
            id: wordmark

            text: "KognogOS"
            color: "#cdd6f4"                       // Catppuccin text
            font.pointSize: Kirigami.Theme.defaultFont.pointSize * 1.6
            font.weight: Font.Light
            font.letterSpacing: Kirigami.Units.gridUnit * 0.35

            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: logo.bottom
            anchors.topMargin: Kirigami.Units.gridUnit
        }

        Image {
            id: spinner

            source: "images/spinner.png"
            smooth: true
            sourceSize.width: Kirigami.Units.gridUnit * 3
            sourceSize.height: Kirigami.Units.gridUnit * 3

            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: wordmark.bottom
            anchors.topMargin: Kirigami.Units.gridUnit * 2

            // Counter-clockwise, matching `spinner.angle -= 0.15` in the
            // Plymouth script — the same wheel, still turning.
            RotationAnimator on rotation {
                from: 360
                to: 0
                duration: 3000
                loops: Animation.Infinite
                running: Kirigami.Units.longDuration > 1
            }
        }

        // Progress rule — the GRUB band's blue → ember sweep, reduced to
        // a hairline. Fills as Plasma reports stages.
        Rectangle {
            id: track

            width: Kirigami.Units.gridUnit * 18
            height: Math.max(2, Kirigami.Units.gridUnit * 0.15)
            radius: height / 2
            color: "#313244"                       // Catppuccin surface0

            anchors.horizontalCenter: parent.horizontalCenter
            anchors.bottom: parent.bottom
            anchors.bottomMargin: Kirigami.Units.gridUnit * 6

            Rectangle {
                id: fill

                height: parent.height
                radius: parent.radius
                anchors.left: parent.left

                width: parent.width * Math.max(0, Math.min(1, (root.stage - 1) / 5))

                gradient: Gradient {
                    orientation: Gradient.Horizontal
                    GradientStop { position: 0.0; color: "#0363ef" }   // logo blue
                    GradientStop { position: 1.0; color: "#d9400e" }   // logo ember
                }

                Behavior on width {
                    NumberAnimation {
                        duration: Kirigami.Units.longDuration * 2
                        easing.type: Easing.InOutQuad
                    }
                }
            }
        }
    }

    OpacityAnimator {
        id: contentFade
        target: content
        from: 0
        to: 1
        duration: Kirigami.Units.veryLongDuration
        easing.type: Easing.InOutQuad
        running: false
    }

    OpacityAnimator {
        id: outroFade
        target: content
        from: 1
        to: 0
        duration: Kirigami.Units.longDuration
        easing.type: Easing.InOutQuad
        running: false
    }
}
