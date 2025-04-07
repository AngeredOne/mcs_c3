# agents/filesystem_agent.py

from core.agent import Agent
from core.task import Task

class FilesystemAgent(Agent):
    def __init__(self):
        super().__init__(name="filesystem_agent")
        self.role = "filesystem_operator"

    def handle_task(self, task: Task):
        action = task.parameters.get("action")
        params = task.parameters.get("params", {})

        if action == "diff_file":
            # Специальная логика для диффа
            diff = self.app.run_command("diff_file", path=params["path"], new_content=params["new_content"])
            task.parameters["diff"] = diff
            return diff

        elif action == "write_file":
            # Логика записи файла
            if not task.parameters.get("approved", False):
                raise PermissionError("Change not approved. Write operation denied.")
            return self.app.run_command("write_file", path=params["path"], content=params["new_content"])

        elif action == "read_file":
            # Логика чтения файла
            content = self.app.run_command("read_file", path=params["path"])
            task.parameters["current_content"] = content
            return content

        else:
            # Любое другое действие
            return self.app.run_command(action, **params)
