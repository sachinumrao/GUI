from cx_Freeze import setup, Executable
import os
os.environ['TCL_LIBRARY'] = ""
os.environ['TK_LIBRARY'] = ""

setup(name = "reandurllib" ,
      version = "0.1" ,
      description = "" ,
      executables = [Executable("main.py")])