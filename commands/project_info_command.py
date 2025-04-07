# commands/project_info_command.py

from core.command import Command
import os

class ProjectInfoCommand(Command):
    def __init__(self):
        super().__init__(name="project_info", description="Provides information about the project structure.")

    def execute(self, base_path: str = "workspace") -> dict:
        structure = {}
        for root, dirs, files in os.walk(base_path):
            rel_root = os.path.relpath(root, base_path)
            structure[rel_root] = {
                "dirs": dirs,
                "files": files
            }
        return structure
