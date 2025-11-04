#!/usr/bin/env pwsh
# Script para iniciar la aplicación en modo desarrollo (PowerShell)
# Guarda este archivo como `start-dev.ps1` en la raíz del proyecto y ejecútalo desde PowerShell.

Set-StrictMode -Version Latest

# Movernos al directorio del script (raíz del proyecto)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $scriptDir

if (-Not (Test-Path ".\venv\Scripts\python.exe")) {
    Write-Error "No se encontró el entorno virtual en .\venv. Crea uno con: py -3 -m venv venv"
    exit 1
}

# Establecer variable de entorno para Flask
$env:FLASK_APP = 'app.py'

# Ejecutar Flask con el intérprete del venv y con recarga/depuración activada
Write-Host "Iniciando Flask en modo desarrollo (debug + reloader)..." -ForegroundColor Cyan
.\venv\Scripts\python.exe -m flask --app app.py --debug run
