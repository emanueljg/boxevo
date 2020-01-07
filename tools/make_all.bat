@echo off
SETLOCAL EnableDelayedExpansion

for %%I in (.) do set base=%%~nxI
if not "!base!"=="tools" (cd tools)

call make_simulation
call make_config_doc
call make_readme

call git commit -a -m "update docs"
call git push

ENDLOCAL
