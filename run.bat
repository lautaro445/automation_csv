@echo off
REM run.bat - Ejecuta Automation CSV en Windows
REM Uso: run.bat simulate | run.bat send [LIMIT]

SET MODE=%1
SET LIMIT=%2

IF "%MODE%"=="" (
    ECHO Uso: run.bat simulate ^| run.bat send [LIMIT]
    EXIT /B 1
)

REM --- Construir la imagen ---
ECHO Construyendo contenedor Docker...
docker build -t automation_csv .

REM --- Preparar argumentos ---
SET ARGS=-i data
IF "%MODE%"=="simulate" SET ARGS=%ARGS% --simulate
IF "%MODE%"=="send" SET ARGS=%ARGS% --send
IF NOT "%LIMIT%"=="" SET ARGS=%ARGS% --limit %LIMIT%

REM --- Ejecutar contenedor ---
ECHO Ejecutando contenedor...
docker run --rm ^
    -v %CD%\data:/app/data ^
    -v %CD%\output:/app/output ^
    -v %CD%\logs:/app/logs ^
    automation_csv %ARGS%

ECHO.
ECHO ✅ Proceso finalizado. Revisá output\ y logs\
