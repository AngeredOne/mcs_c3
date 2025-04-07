# commands/read_file_command.py

from core.command import Command
import os

class ReadFileCommand(Command):
    def __init__(self):
        super().__init__(name="read_file", description="Reads the content of a file.")

    def execute(self, path: str) -> str:
        full_path = os.path.join("workspace", path)
        if not os.path.isfile(full_path):
            raise FileNotFoundError(f"File '{full_path}' does not exist.")
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()
