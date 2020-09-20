import sys
from cx_Freeze import setup, Executable

base = None

if sys.platform == 'win32':
    base = 'Win32GUI'

build_exe_options = {"packages": ["json", "datetime", "pandas", "time",
                                    "requests", "tkinter", "fuzzywuzzy",
                                  "os", 
                                  "openpyxl", 
                                  "scrapy"],
                     "include_files": ['icon_purple.ico', 'logo_purple.png']} 


executables = [Executable(script='buyma_spy.py',
                          icon='icon_purple.ico',
                          base=base)]

setup(name='BuymaSpy',
      version='0.01',
      description='Organise data on buyma.com into Excel spreadsheets',
      executables=executables,
      options = {"build_exe": build_exe_options})
