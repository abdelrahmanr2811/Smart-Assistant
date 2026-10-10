Set WshShell = CreateObject("WScript.Shell")
scriptDir = WshShell.CurrentDirectory
backendDir = scriptDir & "\backend"
WshShell.CurrentDirectory = backendDir
WshShell.Run "python -m uvicorn app.main:app --host 0.0.0.0 --port 8000", 0, False
WScript.Sleep 1500
WshShell.Run "cmd /c start http://localhost:8000", 0, False
