# commands/delete_file_command.py

from core.command import Command
import os

class DeleteFileCommand(Command):
    def __init__(self):
        super().__init__(name="delete_file", description="Deletes a file with confirmation.")

    def execute(self, path: str, confirm: bool = False) -> str:
        full_path = os.path.join("workspace", path)
        if not os.path.isfile(full_path):
            raise FileNotFoundError(f"File '{full_path}' does not exist.")
        if not confirm:
            raise PermissionError("Deletion not confirmed. Set 'confirm=true' to proceed.")
        os.remove(full_path)
        return f"File '{full_path}' deleted successfully."
