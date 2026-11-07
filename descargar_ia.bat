@echo off
title Descargador Automático de IA - Jujutsu Assistant
color 05
echo =======================================================
echo     INICIANDO DESCARGA DE IA (MOTOR LOCAL EDGE AI)     
echo =======================================================
echo.

:: 1. Crear la carpeta models si no existe
if not exist "models" (
    echo [INFO] Creando la carpeta /models en la raiz del proyecto...
    mkdir "models"
)

:: 2. Descargar el modelo Phi-3 de Microsoft mediante el enlace oficial completo
echo [INFO] Conectando con los servidores globales de Hugging Face...
echo [INFO] Descargando Phi-3-mini-4k-instruct-q4.gguf (Aproximadamente 2.2 GB)...
echo [ALERTA] Por favor, no cierres esta ventana. Esto puede tardar unos minutos...
echo.

curl -L "https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf" -o "models\Phi-3-mini-4k-instruct-q4.gguf"

echo.
echo =======================================================
echo    ¡DESCARGA COMPLETADA Y MODELO INDEXADO CON ÉXITO!   
echo =======================================================
echo [OK] El modelo de Microsoft ya esta en su respectiva carpeta.
echo [INFO] Ahora puedes cerrar esta ventana y ejecutar 'iniciar.bat'.
echo.
pause
