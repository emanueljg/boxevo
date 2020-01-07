@echo off
SETLOCAL EnableDelayedExpansion

for %%I in (.) do set base=%%~nxI
if not "!base!"=="tools" (cd tools)

cd ..
copy docs\source\*.md docs\source\temp.md
pandoc docs\source\temp.md -o README.md
del docs\source\temp.md

copy /A README.md README_temp.md /B > nul
del README.md
ren README_temp.md README.md

cd tools