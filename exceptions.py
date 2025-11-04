"""
Excepciones personalizadas
Demuestra herencia y jerarquía de excepciones
"""


class TaskManagerException(Exception):
    """Excepción base para el sistema de gestión de tareas"""
    pass


class TaskNotFoundException(TaskManagerException):
    """Se lanza cuando no se encuentra una tarea"""

    def __init__(self, message: str = "Tarea no encontrada"):
        self.message = message
        super().__init__(self.message)


class InvalidTaskDataException(TaskManagerException):
    """Se lanza cuando los datos de la tarea son inválidos"""

    def __init__(self, message: str = "Datos de tarea inválidos"):
        self.message = message
        super().__init__(self.message)


class TaskAlreadyCompletedException(TaskManagerException):
    """Se lanza cuando se intenta completar una tarea ya completada"""

    def __init__(self, message: str = "La tarea ya está completada"):
        self.message = message
        super().__init__(self.message)