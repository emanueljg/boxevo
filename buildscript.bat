@echo off

set /P version="Enter version identifier: " 

echo "REMOVING FOLDER"
rmdir /s /q dist
echo "INSTALLING MAIN SCRIPT - PYVOLUTION.PY"
pyinstaller pyvolution.py --onefile
echo "INSTALLING SCATTER SCRIPT - SCATTER.PY"
pyinstaller scatter.py --onefile
echo "COPYING CONSTANTS.YAML TO DIST"
copy constants.yaml dist
echo "COPYING OPTIMUSFLY.PNG TO DIST"
copy optimusfly.png dist
echo "COPYING DEBUG.BAT TO DIST"
copy debug.bat dist
echo "COPYING DIST TO WORK FOLDER WITH NAME %version%"
Xcopy dist "C:\Users\eman286a\Ystads Kommun\Rosengren Asp Arvid - Gymnasiearbete\%version%\"
echo "ALL DONE!"