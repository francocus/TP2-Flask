# Gestor de Tareas (Flask)

Pequeña aplicación de ejemplo en Flask para gestionar tareas. Este README explica cómo preparar el entorno, instalar dependencias y ejecutar la aplicación en Windows (PowerShell y CMD).

## Requisitos
- Python 3.7+ (recomendado 3.8+). En Windows suele usarse el launcher `py`.
- Git (opcional) si clonaste el repositorio.

## Preparar el entorno (solo una vez)

Abrir PowerShell y situarse en la carpeta del proyecto:

```powershell
cd /d 'C:\Users\franq\OneDrive\TUP\TP2\task_manager_new'
```

Crear un entorno virtual `venv` (si no existe):

```powershell
py -3 -m venv venv
# o: python -m venv venv
```

Activar el entorno virtual (PowerShell):

```powershell
.\venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la ejecución de scripts por la política, ejecutar (una sola vez) para permitir scripts firmados/locales:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
.\venv\Scripts\Activate.ps1
```

Alternativa (sin cambiar política): abrir `cmd.exe` y ejecutar:

```cmd
venv\Scripts\activate.bat
```

## Instalar dependencias

Con el venv activado:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
# si no existe requirements.txt, instalar Flask directamente:
python -m pip install Flask
```

> Nota: ya hay un `requirements.txt` en el proyecto generado tras la instalación inicial.

## Ejecutar la aplicación

Opción A — Ejecutar directamente `app.py` (usa el `app.run(debug=True)` que está en el `if __name__ == '__main__'`):

PowerShell (con venv activado):

```powershell
cd /d 'C:\Users\franq\OneDrive\TUP\TP2\task_manager_new'
# Activar venv si no está activo
.\venv\Scripts\Activate.ps1
# Ejecutar
python app.py
```

Alternativa (sin activar el venv explícitamente):

```powershell
cd /d 'C:\Users\franq\OneDrive\TUP\TP2\task_manager_new'
.\venv\Scripts\python.exe app.py
```

Opción B — Usar la CLI de Flask (con recarga/depuración):

```powershell
cd /d 'C:\Users\franq\OneDrive\TUP\TP2\task_manager_new'
.\venv\Scripts\python.exe -m flask --app app.py --debug run
```

Opción C — Usar los scripts añadidos:

- `start-dev.ps1` — PowerShell (ejecuta `.
un-dev.ps1` o `.egin` desde la raíz).
- `start-dev.cmd` — CMD (doble clic o desde cmd.exe).

Ejecuta uno de ellos desde la raíz del proyecto:

PowerShell:
```powershell
.\start-dev.ps1
```

CMD:
```cmd
start-dev.cmd
```

## Qué esperar
- La app por defecto se sirve en http://127.0.0.1:5000 o en 0.0.0.0:5000 según cómo la ejecutes.
- Si `app.py` contiene `app.run(debug=True)`, el servidor arrancará en modo desarrollo con recarga automática (reload) y verás cambios en plantillas y código cuando guardes los archivos.

## Variables de entorno / Configuración

`app.py` usa una clave secreta para flashes/sesiones:

- `SECRET_KEY`: si quieres cambiarla, exporta una variable de entorno antes de ejecutar:

PowerShell:
```powershell
$env:SECRET_KEY = 'mi_clave_segura'
python app.py
```

CMD:
```cmd
set SECRET_KEY=mi_clave_segura
venv\Scripts\python.exe app.py
```

## Solución de problemas comunes

- Cambios en templates no se ven: asegúrate de ejecutar `python app.py` (o `flask --debug run`) y no tener procesos antiguos en segundo plano. Si no ves cambios, reinicia el servidor (Ctrl+C y vuelve a ejecutar).
- Error al activar venv en PowerShell: ejecuta `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force` (una vez) o usa `cmd.exe` para activar.
- Puerto en uso: si el puerto 5000 está ocupado, el servidor mostrará el error; cierra el proceso que lo usa o cambia el puerto en `app.run(port=XXXX)`.

## Ejecutar tests / comprobaciones (opcional)

No hay tests automáticos en este proyecto por defecto, pero puedes comprobar que la plantilla se carga:

```powershell
.\venv\Scripts\python.exe -c "import jinja2, os; env=jinja2.Environment(loader=jinja2.FileSystemLoader('templates')); print(env.list_templates())"
```

## Contribuciones y mejoras sugeridas

- Mover estilos a `static/css/style.css` y referenciar en `base.html`.
- Añadir comandos Make/Task para tareas habituales.

---

Si querés, puedo añadir un VS Code `launch.json` para iniciar la aplicación con F5, o crear un `requirements-dev.txt` con herramientas útiles. ¿Querés que lo haga?
