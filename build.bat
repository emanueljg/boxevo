rmdir /s /q Boxevo-program

pyinstaller boxevo.py --onefile
pyinstaller scatter.py --onefile

copy config.py dist
copy optimusfly.png dist
copy debug.bat dist

ren dist Boxevo-program
rmdir /s /q build