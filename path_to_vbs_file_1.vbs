Dim WShell
Set WShell = CreateObject("WScript.Shell")
WShell.Run "cloudflared access rdp --hostname ставляем_свой_урл --url rdp://localhost:1111", 0
WScript.Sleep 4000
WShell.Run "mstsc /v:localhost:1111"
Set WShell = Nothing



