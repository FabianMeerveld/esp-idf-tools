@echo off

REM Store the current directory
SET "ORIGINAL_DIR=%CD%"

REM Change to the directory where the batch file is located
CD /D %~dp0

REM Check if ..\esp-idf-v5.3 directory exists
if exist ..\esp-idf-v5.3 (
    REM Call the export.bat script in the esp-idf-v5.3 directory
    CALL ..\esp-idf-v5.3\export.bat
) else (
    REM Output an error message and exit the script
    echo Directory ..\esp-idf-v5.3 does not exist.
    echo Install ESP-idf v5.3 first. or use idf-tools.py install-idf
)

REM Call the local export.bat script
CALL export.bat

REM Change to D: drive
D:

REM Open a new command prompt window
cmd /k

REM Return to the original directory
CD /D "%ORIGINAL_DIR%"
