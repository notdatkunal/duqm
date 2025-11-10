@echo off
setlocal
set "BASEDIR=%~dp0"

"%BASEDIR%python\python.exe" "%BASEDIR%main.py"
pause
endlocal
