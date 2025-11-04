# Sistema de Gestión de Tareas (Flask)

##  Descripción

Este proyecto es una aplicación web sencilla desarrollada con **Flask** que permite gestionar tareas.
El objetivo es demostrar conceptos de **Programación Orientada a Objetos (POO)** aplicados al desarrollo web con Python.

##  Funcionalidades

* Crear tareas con título y descripción
* Listar todas las tareas registradas
* Marcar tareas como completadas
* Eliminar tareas
* Validación de datos de entrada
* Manejo de excepciones personalizadas
* API REST básica para interacción externa

##  Instalación y ejecución

1. **Crear y activar entorno virtual**

   ```bash
   python -m venv venv
   source venv/bin/activate   # En Windows: venv\Scripts\activate
   ```

2. **Instalar dependencias**

   ```bash
   pip install -r requirements.txt
   ```

3. **Iniciar la aplicación**

   ```bash
   python app.py
   ```

4. Abrir el navegador en [http://localhost:5000](http://localhost:5000)

---

##  Estructura del proyecto

```
TP2-Flask/
│
├── app.py                 # Punto de entrada de la aplicación y definición de rutas
├── models.py              # Clases principales y lógica de negocio (POO)
├── exceptions.py          # Manejo de excepciones personalizadas
├── templates/             # Plantillas HTML (interfaz de usuario)
│   └── *.html
├── tasks_data.json        # Archivo de almacenamiento temporal de tareas
├── requirements.txt       # Dependencias del proyecto
├── start-dev.cmd          # Script para ejecutar en Windows
├── start-dev.ps1          # Script PowerShell para desarrollo
└── .gitignore             # Archivos y carpetas ignoradas por Git
```

---

##  Conceptos de POO aplicados

* **Encapsulación:** La clase `Task` agrupa datos y comportamiento.
* **Abstracción:** La clase `TaskManager` gestiona la lógica de negocio sin exponer detalles internos.
* **Herencia:** Las excepciones personalizadas extienden de una clase base.
* **Separación de responsabilidades:** Cada módulo cumple una función clara y específica.

---

##  Autores

Proyecto desarrollado por **Franco Cuscianna, Thiago Cuscianna, Agustin Angelini**.

Materia: *Desarrollo Web con Flask* — **Tecnicatura Universitaria en Programación (UTN Rosario)**.
