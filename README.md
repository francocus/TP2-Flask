# Sistema de Gestión de Tareas - Flask

## Descripción
Aplicación web de ejemplo que demuestra el uso de Flask con Programación Orientada a Objetos.

## Características
- ✅ Crear tareas con título y descripción
- ✅ Listar todas las tareas
- ✅ Marcar tareas como completadas
- ✅ Eliminar tareas
- ✅ Validación de datos
- ✅ Manejo de excepciones personalizadas
- ✅ API REST básica

## Instalación

1. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecutar la aplicación:
```bash
python app.py
```

4. Abrir navegador en: http://localhost:5000

## Estructura del Proyecto
- **app.py**: Aplicación principal y rutas
- **models.py**: Modelos de datos (POO)
- **exceptions.py**: Excepciones personalizadas
- **templates/**: Plantillas HTML

## API REST
- GET /api/tasks - Lista todas las tareas
- GET /api/task/<id> - Obtiene una tarea específica

## Conceptos de POO Demostrados
1. **Encapsulación**: Clase Task encapsula datos y comportamiento
2. **Abstracción**: TaskManager abstrae la lógica de negocio
3. **Herencia**: Jerarquía de excepciones personalizadas
4. **Separación de responsabilidades**: Cada clase tiene un propósito único
