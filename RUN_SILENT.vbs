Set WshShell = CreateObject("WScript.Shell")
backendDir = WshShell.CurrentDirectory & "\backend"
WshShell.CurrentDirectory = backendDir
WshShell.Run "python -m uvicorn app.main:app --host 0.0.0.0 --port 8000", 0, False
