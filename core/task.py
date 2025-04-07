# core/task.py
import uuid
from typing import Dict, Any, List

class Task:
    def __init__(self, description: str, parameters: Dict[str, Any], result: Any = None):
        self.task_id = str(uuid.uuid4())
        self.description = description
        self.parameters = parameters
        self.result = result
        self.role_history: List[Dict[str, str]] = []

    def set_result(self, result: Any):
        self.result = result

    def add_role_history(self, role: str, agent: str):
        self.role_history.append({"role": role, "agent": agent})
