Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
currentDir = fso.GetParentFolderName(WScript.ScriptFullName)
batchFile = chr(34) & currentDir & "\service_runner.bat" & chr(34)
WshShell.Run batchFile, 0, False
Set WshShell = Nothing
