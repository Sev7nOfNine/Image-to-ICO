Set fso = CreateObject("Scripting.FileSystemObject")
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
Set sh = CreateObject("WScript.Shell")
sh.CurrentDirectory = scriptDir
' 0 = fenetre cachee, False = ne pas attendre la fin
sh.Run """" & scriptDir & "\.venv\Scripts\pythonw.exe"" """ & scriptDir & "\image_to_ico.py""", 0, False
