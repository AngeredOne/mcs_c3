# core/session.py

from typing import List
from core.task import Task

class Session:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.history: List[Task] = []

    def add_task(self, task: Task):
        self.history.append(task)

    def get_history(self) -> List[Task]:
        return self.history
