@echo off
SETLOCAL EnableDelayedExpansion

cd /D "%~dp0"

call make_simulation
call make_config_doc
call make_readme

ENDLOCAL
