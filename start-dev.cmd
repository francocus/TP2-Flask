@echo off
:: Script para iniciar la aplicación en modo desarrollo (Windows cmd)
:: Guarda este archivo como start-dev.cmd en la raíz del proyecto y ejecútalo.

cd /d %~dp0
if not exist venv\Scripts\python.exe (
  echo No se encontro el entorno virtual en venv. Crea uno con: py -3 -m venv venv
  exit /b 1
)

set FLASK_APP=app.py
echo Iniciando Flask en modo desarrollo (debug + reloader)...
venv\Scripts\python.exe -m flask --app app.py --debug run