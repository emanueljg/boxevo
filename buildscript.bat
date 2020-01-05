rd /s /q simulation
mkdir simulation\bundle

pyinstaller simulate.py --distpath simulation --onefile
pyinstaller startworld.py --distpath simulation\bundle --onefile
pyinstaller graph.py --distpath simulation\bundle --onefile

copy config.py simulation\bundle
copy optimusfly.png simulation\bundle

PAUSE