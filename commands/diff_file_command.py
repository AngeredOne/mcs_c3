# commands/diff_file_command.py

from core.command import Command
import os
import difflib

class DiffFileCommand(Command):
    def __init__(self):
        super().__init__(name="diff_file", description="Shows a diff between existing and new file content.")

    def execute(self, path: str, new_content: str) -> str:
        full_path = os.path.join("workspace", path)
        if not os.path.isfile(full_path):
            raise FileNotFoundError(f"File '{full_path}' does not exist.")

        with open(full_path, "r", encoding="utf-8") as f:
            old_content = f.read()

        diff = difflib.unified_diff(
            old_content.splitlines(),
            new_content.splitlines(),
            fromfile='current',
            tofile='proposed',
            lineterm=''
        )
        return "\n".join(diff)
