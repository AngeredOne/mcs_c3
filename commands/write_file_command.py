# commands/write_file_command.py

from core.command import Command
import os

class WriteFileCommand(Command):
    def __init__(self):
        super().__init__(name="write_file", description="Writes content to a file.")

    def execute(self, path: str, content: str) -> str:
        full_path = os.path.join("workspace", path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"File '{full_path}' written successfully."
