# commands/list_directory_command.py

from core.command import Command
import os

class ListDirectoryCommand(Command):
    def __init__(self):
        super().__init__(name="list_directory", description="Lists contents of a directory.")

    def execute(self, path: str = "") -> list:
        full_path = os.path.join("workspace", path)
        if not os.path.isdir(full_path):
            raise NotADirectoryError(f"Directory '{full_path}' does not exist.")
        return os.listdir(full_path)
