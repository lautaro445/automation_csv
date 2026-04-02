@echo off
REM run.bat - Run Automation CSV on Windows
REM Usage: run.bat [simulate|send] [LIMIT]

SET MODE=%1
SET LIMIT=%2

REM Default to simulate if no mode provided
IF "%MODE%"=="" SET MODE=simulate

IF NOT "%MODE%"=="simulate" IF NOT "%MODE%"=="send" (
    ECHO Usage: run.bat [simulate|send] [LIMIT]
    EXIT /B 1
)

ECHO Building Docker container...
docker build -t automation_csv .

REM Prepare arguments
SET ARGS=-i data
IF "%MODE%"=="simulate" SET ARGS=%ARGS% --simulate
IF "%MODE%"=="send" SET ARGS=%ARGS% --send
IF NOT "%LIMIT%"=="" SET ARGS=%ARGS% --limit %LIMIT%

ECHO Executing container...
docker run --rm ^
    -v %CD%\data:/app/data ^
    -v %CD%\output:/app/output ^
    -v %CD%\logs:/app/logs ^
    automation_csv %ARGS%

ECHO.
ECHO Process finished! Check 'output\' and 'logs\' folders.
