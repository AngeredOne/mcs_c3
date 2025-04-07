# agents/inner_developer_agent.py

from core.agent import Agent
from core.task import Task

class InnerDeveloperAgent(Agent):
    def __init__(self):
        super().__init__(name="inner_developer_agent")
        self.role = "inner_developer"

    def handle_task(self, task: Task):
        current_content = task.parameters.get("current_content")
        if current_content is None:
            # Если нет текущего содержимого — надо сначала прочитать файл
            path = task.parameters["path"]
            current_content = self.app.run_command("read_file", path=path)
            task.parameters["current_content"] = current_content

        # Простая генерация нового содержимого
        new_content = f"{current_content}\n# Appended by InnerDeveloperAgent"
        task.parameters["new_content"] = new_content

        return {"new_content": new_content}
