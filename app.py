"""
Sistema de Gestión de Tareas - Ejemplo Flask con POO
Demostración de arquitectura orientada a objetos
"""

import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import TaskManager
from exceptions import TaskNotFoundException, InvalidTaskDataException, TaskAlreadyCompletedException

# Crear aplicación Flask
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'clave-super-secreta-cambiar-en-produccion')

# Inicializar el gestor de tareas con persistencia sencilla en disco
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
task_manager = TaskManager(storage_path=os.path.join(BASE_DIR, 'tasks_data.json'))


@app.route('/')
def index():
    """Página principal - Lista todas las tareas"""
    tasks = task_manager.get_all_tasks()
    stats = task_manager.get_statistics()
    return render_template('index.html', tasks=tasks, stats=stats)


@app.route('/api/tasks', methods=['GET'])
def api_get_tasks():
    """API REST - Obtener todas las tareas en formato JSON"""
    tasks = task_manager.get_all_tasks()
    return jsonify([task.to_dict() for task in tasks])


@app.route('/task/create', methods=['POST'])
def create_task():
    """Crear una nueva tarea"""
    try:
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()

        # Validación básica
        if not title:
            raise InvalidTaskDataException("El título es obligatorio")

        # Crear tarea usando el gestor
        task = task_manager.create_task(title, description)
        flash(f'Tarea "{task.title}" creada exitosamente', 'success')

    except InvalidTaskDataException as e:
        flash(str(e), 'error')
    except Exception as e:
        flash(f'Error inesperado: {str(e)}', 'error')

    return redirect(url_for('index'))


@app.route('/task/<int:task_id>/complete', methods=['POST'])
def complete_task(task_id):
    """Marcar tarea como completada"""
    try:
        task = task_manager.complete_task(task_id)
        flash(f'Tarea "{task.title}" marcada como completada', 'success')
    except TaskNotFoundException as e:
        flash(str(e), 'error')
    except TaskAlreadyCompletedException as e:
        flash(str(e), 'warning')

    return redirect(url_for('index'))


@app.route('/task/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    """Eliminar una tarea"""
    try:
        task_manager.delete_task(task_id)
        flash('Tarea eliminada exitosamente', 'success')
    except TaskNotFoundException as e:
        flash(str(e), 'error')

    return redirect(url_for('index'))


@app.route('/api/task/<int:task_id>', methods=['GET'])
def api_get_task(task_id):
    """API REST - Obtener una tarea específica"""
    try:
        task = task_manager.get_task(task_id)
        return jsonify(task.to_dict())
    except TaskNotFoundException as e:
        return jsonify({'error': str(e)}), 404


@app.route('/task/<int:task_id>/reopen', methods=['POST'])
def reopen_task(task_id):
    """Marcar una tarea completada como pendiente nuevamente"""
    try:
        task = task_manager.get_task(task_id)
        if not task.completed:
            flash('La tarea ya estaba pendiente', 'info')
        else:
            task_manager.reopen_task(task_id)
            flash(f'Tarea "{task.title}" marcada como pendiente', 'success')
    except TaskNotFoundException as e:
        flash(str(e), 'error')

    return redirect(url_for('index'))


@app.route('/api/tasks', methods=['POST'])
def api_create_task():
    """API REST - Crear una tarea usando JSON"""
    payload = request.get_json(silent=True) or {}
    title = (payload.get('title') or '').strip()
    description = (payload.get('description') or '').strip()

    try:
        task = task_manager.create_task(title, description)
        return jsonify(task.to_dict()), 201
    except InvalidTaskDataException as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/task/<int:task_id>', methods=['PUT', 'PATCH'])
def api_update_task(task_id):
    """API REST - Actualizar título, descripción o estado de la tarea"""
    payload = request.get_json(silent=True) or {}
    raw_title = payload.get('title')
    raw_description = payload.get('description')
    completed = payload.get('completed') if 'completed' in payload else None

    title = raw_title.strip() if isinstance(raw_title, str) else None
    description = (
        raw_description.strip() if isinstance(raw_description, str) else None
    )

    try:
        task = task_manager.update_task(task_id, title=title, description=description)
        if completed is True and not task.completed:
            task = task_manager.complete_task(task_id)
        elif completed is False and task.completed:
            task = task_manager.reopen_task(task_id)
        return jsonify(task.to_dict()), 200
    except InvalidTaskDataException as e:
        return jsonify({'error': str(e)}), 400
    except TaskNotFoundException as e:
        return jsonify({'error': str(e)}), 404
    except TaskAlreadyCompletedException as e:
        return jsonify({'error': str(e)}), 409


@app.route('/api/task/<int:task_id>/complete', methods=['POST'])
def api_complete_task(task_id):
    """API REST - Marcar tarea como completada"""
    try:
        task = task_manager.complete_task(task_id)
        return jsonify(task.to_dict()), 200
    except TaskNotFoundException as e:
        return jsonify({'error': str(e)}), 404
    except TaskAlreadyCompletedException as e:
        return jsonify({'error': str(e)}), 409


@app.route('/api/task/<int:task_id>/reopen', methods=['POST'])
def api_reopen_task(task_id):
    """API REST - Reabrir una tarea"""
    try:
        task = task_manager.reopen_task(task_id)
        return jsonify(task.to_dict()), 200
    except TaskNotFoundException as e:
        return jsonify({'error': str(e)}), 404


@app.route('/api/task/<int:task_id>', methods=['DELETE'])
def api_delete_task(task_id):
    """API REST - Eliminar una tarea"""
    try:
        task_manager.delete_task(task_id)
        return '', 204
    except TaskNotFoundException as e:
        return jsonify({'error': str(e)}), 404


@app.errorhandler(404)
def page_not_found(e):
    """Manejo de error 404"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    """Manejo de error 500"""
    return render_template('500.html'), 500


if __name__ == '__main__':
    # Crear tareas de ejemplo solo cuando la lista está vacía
    if not task_manager.get_all_tasks():
        task_manager.create_task(
            "Estudiar Flask",
            "Revisar documentación y hacer ejemplos prácticos"
        )
        task_manager.create_task(
            "Preparar presentación",
            "Crear diapositivas y código de ejemplo"
        )

    # Ejecutar aplicación en modo desarrollo
    app.run(debug=True, host='0.0.0.0', port=5000)