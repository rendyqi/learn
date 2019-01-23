DIM objShell

set objShell=wscript.createObject("wscript.shell")

iReturn=objShell.Run("python run.py", 0, TRUE) 