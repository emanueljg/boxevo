@echo off

rd /s /q simulation

curl -L -O https://codeload.github.com/NihilistBrew/boxevo/zip/master
tar xf master

xcopy boxevo-master\simulation simulation /i /s
rd /s /q boxevo-master
del master
PAUSE