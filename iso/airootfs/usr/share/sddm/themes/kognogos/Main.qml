/*
    KognogOS SDDM greeter.

    A Catppuccin Mocha field, one card floating on it behind a mauve edge
    and a soft shadow, the tier emblem down the card's left edge, and the
    login controls beside it. User and session are both chosen from
    dropdowns; neither is typed. Session picker sits below the card.

    Written against plain QtQuick only -- no SddmComponents, no
    QtQuick.Controls, no QtQuick.Effects -- because the greeter runs
    before a session exists and a missing QML module there means a black
    screen with no way into the machine. That is also why the shadow is
    built from stacked translucent rectangles rather than a blur: the
    blur lives in QtQuick.Effects, and it is not worth the risk.

    Everything is reachable by keyboard: Tab walks user -> password ->
    buttons -> session and wraps, Up/Down move a dropdown's selection,
    Enter or Space opens one, Escape closes it, and the focused control
    carries a blue ring.

    Model roles are read through invisible Repeaters and cached into plain
    JavaScript arrays rather than via numeric role indices. SDDM's role
    enums have gained members between releases, so a hardcoded role number
    renders blank on the versions it does not match -- which is exactly
    how the session line came to show nothing at all.

    SPDX-FileCopyrightText: 2026 Javier
    SPDX-License-Identifier: GPL-3.0-or-later
*/

import QtQuick 2.15

Rectangle {
    id: root

    width: 1920
    height: 1080
    color: config.background || "#1e1e2e"

    readonly property int pad: parseInt(config.cardPadding) || 44
    readonly property int logoSize: parseInt(config.logoSize) || 256
    readonly property string uiFont: config.font || "Noto Sans"
    readonly property int cardRadius: parseInt(config.cardRadius) || 0

    readonly property int shadowLayers: parseInt(config.shadowLayers) || 14
    readonly property int shadowSpread: parseInt(config.shadowSpread) || 48
    readonly property int shadowOffset: parseInt(config.shadowOffset) || 14
    readonly property real shadowOpacity: parseFloat(config.shadowOpacity) || 0.055

    property int sessionIndex: 0
    property int userIndex: 0
    property string errorText: ""

    // Only one list may be open at a time, or they overlap each other.
    property var openList: null
    function closeLists(except) {
        if (root.openList && root.openList !== except)
            root.openList.listOpen = false
        root.openList = except
    }

    // ── model name caches ─────────────────────────────────────────────

    Item {
        id: users
        visible: false

        property var labels: []     // what the human sees
        property var logins: []     // what sddm.login() is given

        Repeater {
            id: userRepeater
            model: userModel
            delegate: Item {
                // Guarded at every step: a role that does not exist on
                // this SDDM reads as undefined, not as an error, and the
                // failure shows up as a blank line rather than a crash.
                property string login: (typeof model.name !== "undefined"
                                        && model.name) ? String(model.name) : ""
                property string label: {
                    var real = (typeof model.realName !== "undefined"
                                && model.realName) ? String(model.realName) : ""
                    return real.length > 0 ? real : login
                }
            }
        }

        function rebuild() {
            var L = [], G = []
            for (var i = 0; i < userRepeater.count; i++) {
                var it = userRepeater.itemAt(i)
                L.push(it && it.label.length > 0 ? it.label : "User " + (i + 1))
                G.push(it ? it.login : "")
            }
            labels = L
            logins = G
        }
    }

    Item {
        id: sessions
        visible: false

        property var labels: []

        Repeater {
            id: sessionRepeater
            model: sessionModel
            delegate: Item {
                property string label: {
                    if (typeof model.name !== "undefined" && model.name)
                        return String(model.name)
                    if (typeof model.display !== "undefined" && model.display)
                        return String(model.display)
                    return ""
                }
            }
        }

        function rebuild() {
            var L = []
            for (var i = 0; i < sessionRepeater.count; i++) {
                var it = sessionRepeater.itemAt(i)
                // Never blank. A session the greeter cannot name is still
                // a session the user must be able to pick.
                L.push(it && it.label.length > 0 ? it.label : "Session " + (i + 1))
            }
            labels = L
        }
    }

    // ── shared building blocks ────────────────────────────────────────

    /*
        The dropdown caret, DRAWN rather than typed.

        This used to be the character "▾" (U+25BE) set in the theme font.
        Noto Sans does not contain that glyph -- checked against the font
        file itself, not assumed -- so it rendered as an empty tofu box.
        Nobody ever saw it, because the old code only drew a caret when
        more than one session existed and this machine has exactly one; it
        would have appeared the first time a second session was installed.

        A greeter cannot depend on a glyph being present in whatever font
        it is handed. This is a path. It cannot go missing.
    */
    component Caret: Canvas {
        id: cv

        property color fill: "#cdd6f4"

        implicitWidth: 11
        implicitHeight: 6

        onFillChanged: requestPaint()
        onPaint: {
            var ctx = getContext("2d")
            ctx.reset()
            ctx.fillStyle = cv.fill
            ctx.beginPath()
            ctx.moveTo(0, 0)
            ctx.lineTo(width, 0)
            ctx.lineTo(width / 2, height)
            ctx.closePath()
            ctx.fill()
        }
    }

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

    /*
        A dropdown that always shows its current value.

        It renders the caret and opens its list even when there is only
        ONE entry. That is deliberate: a control that silently becomes
        inert at count == 1 looks broken, and it hides from the user the
        fact that a choice exists at all. One entry simply means a list
        with one row in it.
    */
    component Dropdown: FocusScope {
        id: dd

        property var labels: []
        property int currentIndex: 0
        property string emptyText: "None available"
        property bool listOpen: false
        property bool flush: false      // align text to the outer edge

        readonly property int count: dd.labels ? dd.labels.length : 0
        readonly property string currentLabel:
            (dd.count > 0 && dd.currentIndex >= 0 && dd.currentIndex < dd.count)
            ? dd.labels[dd.currentIndex] : dd.emptyText

        implicitHeight: 44
        activeFocusOnTab: true
        z: dd.listOpen ? 100 : 0

        function toggle() {
            if (dd.count === 0) return
            dd.listOpen = !dd.listOpen
            root.closeLists(dd.listOpen ? dd : null)
        }

        function step(delta) {
            if (dd.count === 0) return
            var n = dd.currentIndex + delta
            if (n < 0) n = dd.count - 1
            if (n >= dd.count) n = 0
            dd.currentIndex = n
        }

        Keys.onPressed: function (event) {
            if (event.key === Qt.Key_Return || event.key === Qt.Key_Enter
                    || event.key === Qt.Key_Space) {
                dd.toggle(); event.accepted = true
            } else if (event.key === Qt.Key_Down) {
                dd.step(1); event.accepted = true
            } else if (event.key === Qt.Key_Up) {
                dd.step(-1); event.accepted = true
            } else if (event.key === Qt.Key_Escape) {
                dd.listOpen = false; event.accepted = true
            }
        }

        Rectangle {
            id: ddBox
            anchors.fill: parent
            radius: 3
            color: dd.flush ? "transparent" : config.fieldColor
            border.width: dd.activeFocus ? 2 : (dd.flush ? 0 : 0)
            border.color: config.fieldFocusColor

            Text {
                id: ddText
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: parent.left
                anchors.leftMargin: dd.flush ? 8 : 14
                // Flush mode hugs: the caret follows the text instead of
                // being pinned to the far edge, where it read as an
                // unrelated mark floating in space.
                anchors.right: dd.flush ? undefined : caret.left
                anchors.rightMargin: 8
                elide: Text.ElideRight
                text: dd.currentLabel
                color: dd.flush
                       ? ((ddMouse.containsMouse || dd.activeFocus)
                          ? config.footerHoverColor : config.footerTextColor)
                       : config.fieldTextColor
                font.family: root.uiFont
                font.pixelSize: dd.flush ? 14 : 15
            }

            // Always drawn. The caret IS the affordance -- it is what
            // tells you this is a list and not a label.
            Caret {
                id: caret
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: dd.flush ? ddText.right : undefined
                anchors.leftMargin: dd.flush ? 10 : 0
                anchors.right: dd.flush ? undefined : parent.right
                anchors.rightMargin: dd.flush ? 0 : 14
                fill: ddText.color
                opacity: dd.count > 0 ? 1.0 : 0.35
            }

            MouseArea {
                id: ddMouse
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onClicked: {
                    dd.forceActiveFocus()
                    dd.toggle()
                }
            }
        }

        Rectangle {
            id: ddList

            visible: dd.listOpen
            anchors.top: ddBox.bottom
            anchors.topMargin: 4
            anchors.left: ddBox.left
            width: dd.flush ? 320 : ddBox.width
            height: Math.min(dd.count, 6) * 36 + 8
            color: config.listColor
            border.width: 1
            border.color: config.listBorderColor
            radius: 3

            ListView {
                anchors.fill: parent
                anchors.margins: 4
                clip: true
                model: dd.count
                currentIndex: dd.currentIndex

                delegate: Rectangle {
                    width: ListView.view.width
                    height: 36
                    radius: 2
                    color: rowMouse.containsMouse
                           ? config.accentColor
                           : (index === dd.currentIndex ? config.fieldColor
                                                        : "transparent")

                    Text {
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.left: parent.left
                        anchors.leftMargin: 10
                        anchors.right: parent.right
                        anchors.rightMargin: 10
                        elide: Text.ElideRight
                        // Read from the cached array, not from a model
                        // role, for the same reason the caches exist.
                        text: dd.labels[index]
                        color: rowMouse.containsMouse ? config.accentTextColor
                                                      : config.fieldTextColor
                        font.family: root.uiFont
                        font.pixelSize: 14
                    }

                    MouseArea {
                        id: rowMouse
                        anchors.fill: parent
                        hoverEnabled: true
                        cursorShape: Qt.PointingHandCursor
                        onClicked: {
                            dd.currentIndex = index
                            dd.listOpen = false
                            root.closeLists(null)
                        }
                    }
                }
            }
        }
    }

    // ── the shadow ────────────────────────────────────────────────────
    // Declared BEFORE the card so it paints underneath it. Each layer is
    // a little larger and a little fainter than the last; where they
    // overlap the alpha accumulates, which is what produces the falloff.

    Repeater {
        model: root.shadowLayers

        delegate: Rectangle {
            readonly property real t: (index + 1) / root.shadowLayers

            width: card.width + t * root.shadowSpread * 2
            height: card.height + t * root.shadowSpread * 2
            x: card.x - t * root.shadowSpread
            y: card.y - t * root.shadowSpread + root.shadowOffset
            radius: root.cardRadius + t * root.shadowSpread
            color: config.shadowColor || "#11111b"
            opacity: root.shadowOpacity * (1.0 - t) * (1.0 - t)
        }
    }

    // ── the card ──────────────────────────────────────────────────────

    Rectangle {
        id: card

        anchors.centerIn: parent
        width: parseInt(config.cardWidth) || 880
        height: parseInt(config.cardHeight) || 400
        color: config.cardColor
        radius: root.cardRadius

        border.width: parseInt(config.cardBorderWidth) || 1
        border.color: config.cardBorderColor || "#cba6f7"

        // Emblem down the left edge, drawn at its native 256x256 -- see
        // the geometry note in theme.conf for why the size is not free.
        // Vertically CENTRED rather than pinned to the top padding: the
        // card grew when the username became a dropdown, and pinning left
        // the emblem sitting high with dead space beneath it.
        Image {
            id: emblem

            source: config.logo || "assets/logo.png"
            smooth: false                     // keep the pixel-art edge
            fillMode: Image.PreserveAspectFit

            x: root.pad
            anchors.verticalCenter: parent.verticalCenter
            width: root.logoSize
            height: root.logoSize
        }

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
                    text: "User"
                    color: config.cardTextColor
                    font.family: root.uiFont
                    font.pixelSize: 13
                    font.weight: Font.DemiBold
                }

                Dropdown {
                    id: userPicker
                    width: parent.width
                    labels: users.labels
                    emptyText: "No users found"
                    KeyNavigation.tab: passField
                    KeyNavigation.backtab: sessionPicker
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
                    KeyNavigation.backtab: userPicker
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

    Row {
        anchors.left: card.left
        anchors.top: card.bottom
        anchors.topMargin: 22
        spacing: 8

        Text {
            anchors.verticalCenter: parent.verticalCenter
            text: "Session:"
            color: config.footerTextColor
            font.family: root.uiFont
            font.pixelSize: 14
        }

        Dropdown {
            id: sessionPicker
            flush: true
            width: 300
            height: 26
            labels: sessions.labels
            emptyText: "No sessions installed"
            KeyNavigation.tab: userPicker
            KeyNavigation.backtab: shutdownButton
        }
    }

    // ── behaviour ─────────────────────────────────────────────────────

    function attemptLogin() {
        root.errorText = ""

        var i = userPicker.currentIndex
        if (i < 0 || i >= users.logins.length || users.logins[i] === "") {
            root.errorText = "No user selected"
            return
        }
        sddm.login(users.logins[i], passField.text, sessionPicker.currentIndex)
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
        users.rebuild()
        sessions.rebuild()

        // Preselect the last user by NAME rather than by a remembered
        // index: the index is only meaningful against the same ordering,
        // and the ordering is not promised to be stable.
        var last = (typeof userModel.lastUser !== "undefined")
                   ? String(userModel.lastUser) : ""
        var ui = users.logins.indexOf(last)
        userPicker.currentIndex = ui >= 0 ? ui : 0

        // Clamp rather than trust: lastIndex has been seen out of range,
        // and an out-of-range index is what renders the label blank.
        var si = (typeof sessionModel.lastIndex !== "undefined")
                 ? sessionModel.lastIndex : 0
        if (si < 0 || si >= sessions.labels.length) si = 0
        sessionPicker.currentIndex = si

        passField.focusInput()
    }
}
