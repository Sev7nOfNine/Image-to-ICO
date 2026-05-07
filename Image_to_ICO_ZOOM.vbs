Set fso = CreateObject("Scripting.FileSystemObject")
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
Set sh = CreateObject("WScript.Shell")
sh.CurrentDirectory = scriptDir
sh.Run """" & scriptDir & "\.venv\Scripts\pythonw.exe"" """ & scriptDir & "\image_to_ico_zoom.py""", 0, False
