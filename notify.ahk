for n, param in A_Args {
    TrayTip You were pinged!, %param%
    Sleep 5000   ; display for 5 seconds.

    HideTrayTip() {
        TrayTip  ; Attempt to hide it the normal way.
        if SubStr(A_OSVersion,1,3) = "10." {
            Menu Tray, NoIcon
            Sleep 200  ; It may be necessary to adjust this sleep.
            Menu Tray, Icon
        }
    }
}