@echo off
SETLOCAL EnableDelayedExpansion

for %%I in (.) do set base=%%~nxI
if not "!base!"=="tools" (cd tools)

make_simulation
make_config_doc
make_readme

git add ..\*
ENDLOCAL
