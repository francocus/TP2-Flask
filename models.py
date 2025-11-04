"""
Modelos de datos - Implementación con POO
Demuestra encapsulación, abstracción y responsabilidad única
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from exceptions import (
    InvalidTaskDataException,
    TaskAlreadyCompletedException,
    TaskNotFoundException,
)


logger = logging.getLogger(__name__)


class Task:
    """
    Clase que representa una tarea individual
    Encapsula los datos y comportamiento de una tarea
    """

    def __init__(
        self,
        task_id: int,
        title: str,
        description: str = "",
        *,
        completed: bool = False,
        created_at: Optional[datetime] = None,
        completed_at: Optional[datetime] = None,
    ):
        """
        Constructor de la clase Task

        Args:
            task_id: Identificador único de la tarea
            title: Título de la tarea
            description: Descripción opcional de la tarea
        """
        self._validate_data(title)
        self.id = task_id
        self.title = title
        self.description = description
        self.completed = completed
        self.created_at = created_at or datetime.now()
        self.completed_at: Optional[datetime] = completed_at

    @staticmethod
    def _validate_data(title: str) -> None:
        """Validación de datos de entrada"""
        if not title or not title.strip():
            raise InvalidTaskDataException(
                "El título de la tarea no puede estar vacío"
            )
        if len(title) > 200:
            raise InvalidTaskDataException(
                "El título no puede exceder 200 caracteres"
            )

    def mark_as_completed(self) -> None:
        """Marca la tarea como completada"""
        if self.completed:
            raise TaskAlreadyCompletedException()
        self.completed = True
        self.completed_at = datetime.now()

    def mark_as_pending(self) -> None:
        """Marca la tarea como pendiente"""
        self.completed = False
        self.completed_at = None

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Crea una tarea desde un diccionario persistido"""
        created_at = (
            datetime.fromisoformat(data["created_at"])
            if data.get("created_at")
            else None
        )
        completed_at = (
            datetime.fromisoformat(data["completed_at"])
            if data.get("completed_at")
            else None
        )
        return cls(
            task_id=int(data["id"]),
            title=data["title"],
            description=data.get("description", ""),
            completed=bool(data.get("completed", False)),
            created_at=created_at,
            completed_at=completed_at,
        )

    def to_dict(self) -> dict:
        """
        Convierte la tarea a un diccionario
        Útil para serialización JSON
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

    def __repr__(self) -> str:
        """Representación en string de la tarea"""
        status = "✓" if self.completed else "○"
        return f"<Task {self.id}: {status} {self.title}>"


class TaskManager:
    """
    Clase gestora de tareas - Implementa el patrón Repository
    Centraliza la lógica de negocio y acceso a datos
    """

    def __init__(self, storage_path: Optional[str] = None):
        """Inicializa el gestor y, si es posible, carga datos persistidos"""
        self._tasks: List[Task] = []
        self._next_id = 1
        self._storage_path = Path(storage_path or "tasks_data.json")
        self._load_tasks()

    def create_task(self, title: str, description: str = "") -> Task:
        """
        Crea una nueva tarea

        Args:
            title: Título de la tarea
            description: Descripción opcional

        Returns:
            La tarea creada

        Raises:
            InvalidTaskDataException: Si los datos son inválidos
        """
        task = Task(self._next_id, title, description)
        self._tasks.append(task)
        self._next_id += 1
        self._save_tasks()
        return task

    def get_task(self, task_id: int) -> Task:
        """
        Obtiene una tarea por su ID

        Args:
            task_id: ID de la tarea a buscar

        Returns:
            La tarea encontrada

        Raises:
            TaskNotFoundException: Si la tarea no existe
        """
        task = self._find_task_by_id(task_id)
        if task is None:
            raise TaskNotFoundException(f"Tarea con ID {task_id} no encontrada")
        return task

    def get_all_tasks(self) -> List[Task]:
        """Retorna todas las tareas"""
        return self._tasks.copy()

    def get_pending_tasks(self) -> List[Task]:
        """Retorna solo las tareas pendientes"""
        return [task for task in self._tasks if not task.completed]

    def get_completed_tasks(self) -> List[Task]:
        """Retorna solo las tareas completadas"""
        return [task for task in self._tasks if task.completed]

    def complete_task(self, task_id: int) -> Task:
        """
        Marca una tarea como completada

        Args:
            task_id: ID de la tarea

        Returns:
            La tarea completada

        Raises:
            TaskNotFoundException: Si la tarea no existe
        """
        task = self.get_task(task_id)
        task.mark_as_completed()
        self._save_tasks()
        return task

    def reopen_task(self, task_id: int) -> Task:
        """Vuelve a marcar una tarea como pendiente"""
        task = self.get_task(task_id)
        if task.completed:
            task.mark_as_pending()
            self._save_tasks()
        return task

    def update_task(
        self,
        task_id: int,
        *,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Task:
        """Actualiza los datos básicos de una tarea existente"""
        task = self.get_task(task_id)
        if title is not None:
            Task._validate_data(title)
            task.title = title
        if description is not None:
            task.description = description
        self._save_tasks()
        return task

    def delete_task(self, task_id: int) -> None:
        """
        Elimina una tarea

        Args:
            task_id: ID de la tarea a eliminar

        Raises:
            TaskNotFoundException: Si la tarea no existe
        """
        task = self.get_task(task_id)
        self._tasks.remove(task)
        self._save_tasks()

    def _find_task_by_id(self, task_id: int) -> Optional[Task]:
        """Método auxiliar para buscar tarea por ID"""
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def get_statistics(self) -> dict:
        """Retorna estadísticas de las tareas"""
        total = len(self._tasks)
        completed = len(self.get_completed_tasks())
        pending = len(self.get_pending_tasks())

        return {
            'total': total,
            'completed': completed,
            'pending': pending,
            'completion_rate': (completed / total * 100) if total > 0 else 0
        }

    def _load_tasks(self) -> None:
        """Carga tareas persistidas desde disco, si existen"""
        if not self._storage_path.exists():
            return
        try:
            raw_data = self._storage_path.read_text(encoding="utf-8")
        except OSError as exc:
            logger.warning("No se pudo leer el archivo de tareas: %s", exc)
            return
        if not raw_data.strip():
            return
        try:
            payload = json.loads(raw_data)
        except json.JSONDecodeError as exc:
            logger.warning("Archivo de tareas corrupto: %s", exc)
            return
        loaded_tasks: List[Task] = []
        for item in payload:
            try:
                loaded_tasks.append(Task.from_dict(item))
            except (InvalidTaskDataException, KeyError, ValueError) as exc:
                logger.warning("Registro de tarea inválido omitido: %s", exc)
        self._tasks = loaded_tasks
        if self._tasks:
            self._next_id = max(task.id for task in self._tasks) + 1
        else:
            self._next_id = 1

    def _save_tasks(self) -> None:
        """Persiste el listado de tareas a disco"""
        try:
            self._storage_path.parent.mkdir(parents=True, exist_ok=True)
            serialized = json.dumps(
                [task.to_dict() for task in self._tasks],
                ensure_ascii=False,
                indent=2,
            )
            self._storage_path.write_text(serialized, encoding="utf-8")
        except OSError as exc:
            logger.warning("No se pudo guardar el archivo de tareas: %s", exc)