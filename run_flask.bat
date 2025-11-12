@echo off
setlocal
set "BASEDIR=%~dp0"

:: Change to the extracted or script directory
cd /d "%BASEDIR%"

"%BASEDIR%python\python.exe" "%BASEDIR%main.py"
pause
endlocal
