# core/agent.py

from core.task import Task

from typing import Any, TYPE_CHECKING
if TYPE_CHECKING:
    from core.app import CoreApp

class Agent:
    def __init__(self, name: str):
        self.name = name
        self.role = None
        self.app: "CoreApp" = None  # Объявляем тип как строку для аннотации

    def bind_app(self, app: "CoreApp"):
        self.app = app

    def handle_task(self, task: Task) -> Any:
        raise NotImplementedError()
