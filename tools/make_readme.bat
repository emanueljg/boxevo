@echo off

cd ..
copy docs\source\markdowns\*.md docs\source\markdowns\temp.md
pandoc docs\source\markdowns\temp.md -o README.md
del docs\source\markdowns\temp.md

copy /A README.md README_temp.md /B > nul
del README.md
ren README_temp.md README.md

git add README.md

cd tools