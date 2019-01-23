from app import gdb, gpy
import app.models

def getPinyin(content):
    pyList = gpy.spy_string(content)
    spy = '$'+'$'.join(pyList)
    return spy