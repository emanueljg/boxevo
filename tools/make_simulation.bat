@echo off
SETLOCAL EnableDelayedExpansion

cd /D "%~dp0"

cd ..
rd /s /q simulation
md simulation\bundle

pyinstaller src\simulate.py --distpath simulation --hidden-import=pkg_resources.py2_warn --onefile
pyinstaller src\startworld.py --distpath simulation\bundle --hidden-import=pkg_resources.py2_warn --onefile
pyinstaller src\graph.py --distpath simulation\bundle --hidden-import pkg_resources.py2_warn --onefile
pyinstaller src\spreadsheet.py --distpath simulation\bundle --hidden-import=pkg_resources.py2_warn --onefile


copy src\config.py simulation\bundle
xcopy resources simulation\bundle /i

cd tools

ENDLOCAL
