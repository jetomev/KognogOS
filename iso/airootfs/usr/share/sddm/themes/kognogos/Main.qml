/*
    KognogOS SDDM greeter.

    Black field, one borderless card centred on it, the tier emblem down
    the card's left edge, and the login controls left-aligned beside it.
    Session picker floats below the card, on the black.

    Written against plain QtQuick only -- no SddmComponents, no
    QtQuick.Controls -- because the greeter runs before a session exists
    and a missing QML module there means a black screen with no way in.

    Everything is reachable by keyboard: Tab walks username -> password ->
    buttons -> session picker and wraps, Enter activates whatever holds
    focus, and the focused control carries a blue ring.

    SPDX-FileCopyrightText: 2026 Javier
    SPDX-License-Identifier: GPL-3.0-or-later
*/

import QtQuick 2.15

Rectangle {
    id: root

    width: 1920
    height: 1080
    color: config.background || "#000000"

    readonly property int pad: parseInt(config.cardPadding) || 44
    readonly property int logoSize: parseInt(config.logoSize) || 256
    readonly property string uiFont: config.font || "Noto Sans"

    property int sessionIndex: sessionModel.lastIndex
    property string errorText: ""

    // ── shared building blocks ────────────────────────────────────────

    component FlatButton: Rectangle {
        id: btn

        property string label: ""
        property color fill: config.neutralColor
        property color textColor: config.neutralTextColor
        signal clicked()

        activeFocusOnTab: enabled

        implicitWidth: btnLabel.implicitWidth + 34
        implicitHeight: 40
        radius: 3
        opacity: enabled ? 1.0 : 0.4
        color: enabled && (mouse.containsMouse || btn.activeFocus)
               ? Qt.lighter(fill, 1.25) : fill
        border.width: btn.activeFocus ? 2 : 0
        border.color: config.fieldFocusColor

        Behavior on color { ColorAnimation { duration: 90 } }

        Keys.onPressed: function (event) {
            if (event.key === Qt.Key_Return || event.key === Qt.Key_Enter
                    || event.key === Qt.Key_Space) {
                btn.clicked()
                event.accepted = true
            }
        }

        Text {
            id: btnLabel
            anchors.centerIn: parent
            text: btn.label
            color: btn.textColor
            font.family: root.uiFont
            font.pixelSize: 15
            font.weight: Font.DemiBold
        }

        MouseArea {
            id: mouse
            anchors.fill: parent
            hoverEnabled: true
            enabled: btn.enabled
            cursorShape: Qt.PointingHandCursor
            onClicked: {
                btn.forceActiveFocus()
                btn.clicked()
            }
        }
    }

    // FocusScope, not Rectangle: it lets Tab land on the Field and have
    // the inner TextInput actually take the caret.
    component Field: FocusScope {
        id: field

        property alias text: input.text
        property alias echoMode: input.echoMode
        property string placeholder: ""
        signal accepted()

        function focusInput() { input.forceActiveFocus() }

        implicitHeight: 44
        activeFocusOnTab: true

        Rectangle {
            anchors.fill: parent
            radius: 3
            color: config.fieldColor
            border.width: field.activeFocus ? 2 : 0
            border.color: config.fieldFocusColor

            Text {
                anchors.verticalCenter: parent.verticalCenter
                x: 14
                text: field.placeholder
                visible: input.text.length === 0
                color: config.fieldPlaceholderColor
                font.family: root.uiFont
                font.pixelSize: 15
            }

            TextInput {
                id: input
                focus: true
                anchors.fill: parent
                anchors.leftMargin: 14
                anchors.rightMargin: 14
                verticalAlignment: TextInput.AlignVCenter
                color: config.fieldTextColor
                font.family: root.uiFont
                font.pixelSize: 15
                selectByMouse: true
                selectionColor: config.accentColor
                selectedTextColor: config.accentTextColor
                clip: true
                onAccepted: field.accepted()
            }
        }
    }

    // ── the card ──────────────────────────────────────────────────────

    Rectangle {
        id: card

        anchors.centerIn: parent
        width: parseInt(config.cardWidth) || 880
        height: parseInt(config.cardHeight) || 344
        color: config.cardColor
        radius: 0          // rectangular and borderless, per the brief

        // Emblem down the left edge, inset by the same padding on top,
        // left and bottom. Drawn at its native 256x256 -- see the
        // geometry note in theme.conf for why the size is not free.
        Image {
            id: emblem

            source: config.logo || "assets/logo.png"
            smooth: false                     // keep the pixel-art edge
            fillMode: Image.PreserveAspectFit

            x: root.pad
            y: root.pad
            width: root.logoSize
            height: root.logoSize
        }

        // Everything else shares the emblem's top and bottom margins.
        Item {
            id: form

            x: emblem.x + emblem.width + root.pad
            y: root.pad
            width: card.width - x - root.pad
            height: card.height - root.pad * 2

            Column {
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.verticalCenter: parent.verticalCenter
                spacing: 10

                Text {
                    text: "Username"
                    color: config.cardTextColor
                    font.family: root.uiFont
                    font.pixelSize: 13
                    font.weight: Font.DemiBold
                }

                Field {
                    id: userField
                    width: parent.width
                    placeholder: "Username"
                    text: userModel.lastUser
                    KeyNavigation.tab: passField
                    KeyNavigation.backtab: sessionPicker
                    onAccepted: passField.focusInput()
                }

                Text {
                    text: "Password"
                    color: config.cardTextColor
                    font.family: root.uiFont
                    font.pixelSize: 13
                    font.weight: Font.DemiBold
                }

                Field {
                    id: passField
                    width: parent.width
                    placeholder: "Password"
                    echoMode: TextInput.Password
                    KeyNavigation.tab: loginButton
                    KeyNavigation.backtab: userField
                    onAccepted: root.attemptLogin()
                }

                // Reserves its own line so the buttons never jump when a
                // message appears.
                Item {
                    width: parent.width
                    height: 20

                    Text {
                        anchors.verticalCenter: parent.verticalCenter
                        text: root.errorText !== "" ? root.errorText
                              : (keyboard.capsLock ? "Caps Lock is on" : "")
                        color: root.errorText !== "" ? config.errorColor
                                                     : config.cardTextColor
                        font.family: root.uiFont
                        font.pixelSize: 13
                    }
                }

                Row {
                    spacing: 10

                    // The power buttons stay VISIBLE and go disabled when
                    // the daemon reports no capability, rather than
                    // vanishing. Hiding on a failed capability query means
                    // a greeter you cannot shut down from -- and it is
                    // always false under --test-mode, which has no daemon.
                    FlatButton {
                        id: loginButton
                        label: "Log In"
                        fill: config.accentColor
                        textColor: config.accentTextColor
                        KeyNavigation.tab: restartButton
                        KeyNavigation.backtab: passField
                        onClicked: root.attemptLogin()
                    }

                    FlatButton {
                        id: restartButton
                        label: "Restart"
                        fill: config.warningColor
                        textColor: config.warningTextColor
                        enabled: sddm.canReboot
                        KeyNavigation.tab: shutdownButton
                        KeyNavigation.backtab: loginButton
                        onClicked: sddm.reboot()
                    }

                    FlatButton {
                        id: shutdownButton
                        label: "Shut Down"
                        fill: config.dangerColor
                        textColor: config.dangerTextColor
                        enabled: sddm.canPowerOff
                        KeyNavigation.tab: sessionPicker
                        KeyNavigation.backtab: restartButton
                        onClicked: sddm.powerOff()
                    }
                }
            }
        }
    }

    // ── session picker, floating below the card ───────────────────────

    // Names are read through a Repeater rather than sessionModel.data()
    // with a numeric role: SDDM's SessionRole enum has gained members
    // between releases, so a hardcoded role number renders blank on the
    // versions it does not match. `model.name` in a delegate is stable.
    Item {
        id: sessionNames
        visible: false

        Repeater {
            id: sessionNameRepeater
            model: sessionModel
            delegate: Item { property string sessionName: model.name }
        }

        function nameAt(i) {
            var item = sessionNameRepeater.itemAt(i)
            return item ? item.sessionName : ""
        }
    }

    Column {
        // Left-aligned under the card. The -8 cancels the focus ring's own
        // padding so the label reads flush with the card's left edge
        // rather than 8px inside it; the ring simply overhangs.
        anchors.left: card.left
        anchors.leftMargin: -8
        anchors.top: card.bottom
        anchors.topMargin: 22
        spacing: 8

        Item {
            id: sessionPicker

            width: sessionLabel.implicitWidth + 16
            height: sessionLabel.implicitHeight + 10
            activeFocusOnTab: true

            KeyNavigation.tab: userField
            KeyNavigation.backtab: shutdownButton

            Keys.onPressed: function (event) {
                if (event.key === Qt.Key_Return || event.key === Qt.Key_Enter
                        || event.key === Qt.Key_Space) {
                    if (sessionModel.count > 1)
                        sessionList.visible = !sessionList.visible
                    event.accepted = true
                }
            }

            Rectangle {
                anchors.fill: parent
                radius: 3
                color: "transparent"
                border.width: sessionPicker.activeFocus ? 2 : 0
                border.color: config.fieldFocusColor
            }

            Text {
                id: sessionLabel

                anchors.left: parent.left
                anchors.leftMargin: 8
                anchors.verticalCenter: parent.verticalCenter
                // The caret only appears when there is actually something
                // to choose between -- this machine ships one session.
                text: "Session: " + sessionNames.nameAt(root.sessionIndex)
                      + (sessionModel.count > 1 ? "  ▾" : "")
                color: (sessionMouse.containsMouse || sessionPicker.activeFocus)
                       ? config.footerHoverColor : config.footerTextColor
                font.family: root.uiFont
                font.pixelSize: 14
            }

            MouseArea {
                id: sessionMouse
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onClicked: {
                    sessionPicker.forceActiveFocus()
                    if (sessionModel.count > 1)
                        sessionList.visible = !sessionList.visible
                }
            }
        }

        Rectangle {
            id: sessionList

            visible: false
            width: 280
            height: Math.min(sessionModel.count, 6) * 36 + 8
            color: config.fieldColor
            radius: 3

            ListView {
                anchors.fill: parent
                anchors.margins: 4
                clip: true
                model: sessionModel

                delegate: Rectangle {
                    width: ListView.view.width
                    height: 36
                    color: sessionItemMouse.containsMouse ? config.accentColor
                                                          : "transparent"
                    radius: 2

                    Text {
                        anchors.verticalCenter: parent.verticalCenter
                        x: 10
                        text: model.name
                        color: sessionItemMouse.containsMouse
                               ? config.accentTextColor : config.fieldTextColor
                        font.family: root.uiFont
                        font.pixelSize: 14
                    }

                    MouseArea {
                        id: sessionItemMouse
                        anchors.fill: parent
                        hoverEnabled: true
                        cursorShape: Qt.PointingHandCursor
                        onClicked: {
                            root.sessionIndex = index
                            sessionList.visible = false
                        }
                    }
                }
            }
        }
    }

    // ── behaviour ─────────────────────────────────────────────────────

    function attemptLogin() {
        root.errorText = ""
        sddm.login(userField.text, passField.text, root.sessionIndex)
    }

    Connections {
        target: sddm

        function onLoginFailed() {
            root.errorText = "Incorrect username or password"
            passField.text = ""
            passField.focusInput()
        }

        function onLoginSucceeded() {
            root.errorText = ""
        }
    }

    Component.onCompleted: {
        if (userField.text === "")
            userField.focusInput()
        else
            passField.focusInput()
    }
}
