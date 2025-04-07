# core/command.py

from typing import Any

class Command:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def execute(self, **kwargs) -> Any:
        raise NotImplementedError()
