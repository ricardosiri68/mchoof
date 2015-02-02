import sys, os
from cx_Freeze import setup, Executable


def loadViews():
    appdir = os.path.dirname(sys.argv[0])
    paths = []
    views = os.listdir("views")
    for view in views:
        if not "." in view:
            files = os.listdir("views/%s" % view)
            for f in files:
                data_file_name = os.path.join(appdir, "views/%s" % view,f)
                paths.append(data_file_name)
    return paths

def loadModelConf():
    appdir = os.path.dirname(sys.argv[0])
    paths = []
    confs = os.listdir("models/conf")
    for conf in confs:
        if ".xml" in conf: 
            data_file_name = os.path.join(appdir, "models/conf",conf)
            paths.append(data_file_name)
    return paths

def loadDrivers():
    appdir = os.path.dirname(sys.argv[0])
    paths = []
    libs = os.listdir("sqldrivers")
    for lib in libs: 
        data_file_name = os.path.join(appdir, "sqldrivers/",lib)
        paths.append(data_file_name)
    return paths

miselanea = ['port','style.css','icon.ico','libmysql.dll']
paths = loadViews()
paths.extend(loadModelConf())
paths.extend(loadDrivers())
paths.extend(miselanea)


# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"excludes": ["tkinter"],
                     "include_files":paths,
                     "build_exe":"build"}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "rematesTuki",
        version = "0.1",
        description = "systema de gestion de remates locales",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", base=base)])