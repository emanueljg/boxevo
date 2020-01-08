@echo off
SETLOCAL EnableDelayedExpansion

cd /D "%~dp0"

call make_simulation
call make_config_doc
call make_readme

call git commit -a -m "update docs"
call git push

ENDLOCAL
