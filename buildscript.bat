@echo off

set /P version="Enter version identifier: " 

echo REMOVING OLD DIST FOLDER
rmdir /s /q dist
echo INSTALLING MAIN SCRIPT - BOXEVO.PY
pyinstaller boxevo.py --onefile
echo INSTALLING SCATTER SCRIPT - SCATTER.PY
pyinstaller scatter.py --onefile
echo COPYING CONSTANTS.YAML TO DIST
copy config.py dist
echo COPYING OPTIMUSFLY.PNG TO DIST
copy optimusfly.png dist
echo COPYING DEBUG.BAT TO DIST
copy debug.bat dist

echo COPYING SRC TO DIST
mkdir src
copy boxevo.py src
copy buildscript.bat src
copy config.py src
copy game_setup.py src
copy scatter.py src
copy sprite.py src
mv src\ dist\

echo COPYING DIST TO WORK FOLDER WITH NAME %version%
Xcopy /e dist "C:\Users\eman286a\Ystads Kommun\Rosengren Asp Arvid - Gymnasiearbete\%version%\"
echo ALL DONE!