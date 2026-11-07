@echo off
setlocal enabledelayedexpansion

:: ============================================================================
:: ARRANCADOR AUTOMATICO - ASISTENTE HIBRIDO (LOCAL .GGUF + AZURE FOUNDRY)
:: ============================================================================

title Asistente Hibrido IA - Verificador y Arrancador
cd /d "%~dp0"

echo ==========================================================================
echo        INICIALIZADOR DEL ASISTENTE HIBRIDO DE IA (LOCAL / NUBE)
echo ==========================================================================
echo.

:: ----------------------------------------------------------------------------
:: 1. COMPROBAR PYTHON
:: ----------------------------------------------------------------------------
echo [1/5] Verificando instalacion de Python...
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR CRITICO] No se encontro Python en el sistema o no esta en el PATH.
    echo Por favor instala Python 3.10 o superior marcando la casilla Add Python to PATH.
    echo Descarga: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%v in ('python --version 2^>^&1') do set "PY_VER=%%v"
echo       - Detectado: %PY_VER%

:: ----------------------------------------------------------------------------
:: 2. VERIFICAR / ACTIVAR ENTORNO VIRTUAL (.venv si existe)
:: ----------------------------------------------------------------------------
echo [2/5] Comprobando entorno de ejecucion...
if exist ".venv\Scripts\activate.bat" (
    echo       - Activando entorno virtual local .venv...
    call .venv\Scripts\activate.bat
    set "PY_CMD=python"
) else (
    echo       - Utilizando Python del sistema.
    set "PY_CMD=python"
)

:: ----------------------------------------------------------------------------
:: 3. VERIFICAR E INSTALAR DEPENDENCIAS (requirements.txt)
:: ----------------------------------------------------------------------------
echo [3/5] Verificando librerias y dependencias necesarias...
%PY_CMD% -c "import fastapi, uvicorn, pydantic, dotenv, azure.ai.projects, azure.identity, openai, llama_cpp, matplotlib, numpy, PIL" >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo       [AVISO] Faltan librerias requeridas.
    echo       Instalando paquetes desde requirements.txt, esto puede tomar unos minutos...
    echo.
    %PY_CMD% -m pip install --upgrade pip
    %PY_CMD% -m pip install -r requirements.txt
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo [ERROR] Ocurrio un fallo al instalar las dependencias con pip.
        echo Revisa tu conexion a internet o los permisos de instalacion.
        echo.
        pause
        exit /b 1
    )
    echo       [OK] Dependencias instaladas exitosamente.
) else (
    echo       - Todas las librerias estan instaladas y listas.
)

:: ----------------------------------------------------------------------------
:: 4. VERIFICAR CARPETAS Y ARCHIVO .ENV
:: ----------------------------------------------------------------------------
echo [4/5] Verificando estructura de archivos y configuracion...
if not exist "models" (
    echo       - Creando carpeta models para modelos .gguf...
    mkdir models
)

if not exist ".env" (
    if exist ".env.example" (
        echo       - No se encontro .env. Creando uno base a partir de .env.example...
        copy ".env.example" ".env" >nul
        echo       [AVISO] Se creo el archivo .env con la configuracion base.
    ) else (
        echo       [AVISO] No se encontro .env. El servidor funcionara con valores por defecto.
    )
) else (
    echo       - Archivo .env detectado correctamente.
)

:: ----------------------------------------------------------------------------
:: 5. INICIAR EL SERVIDOR Y ABRIR NAVEGADOR
:: ----------------------------------------------------------------------------
echo [5/5] Iniciando el Asistente Hibrido...
echo.
echo ==========================================================================
echo  Servidor en ejecucion: http://127.0.0.1:8000
echo  Presiona Ctrl + C en esta ventana para detener el servidor.
echo ==========================================================================
echo.

:: Abrir navegador en segundo plano tras breve pausa
start "" cmd /c "timeout /t 2 >nul & start http://127.0.0.1:8000"

:: Arrancar servidor FastAPI
%PY_CMD% server.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [AVISO] El servidor se detuvo con codigo de error %ERRORLEVEL%.
    pause
)
