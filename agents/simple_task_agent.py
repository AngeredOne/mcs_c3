# agents/simple_task_agent.py

from core.agent import Agent
from core.task import Task

class SimpleTaskAgent(Agent):
    def __init__(self):
        super().__init__(name="simple_task_agent")
        self.role = "executor"

    def handle_task(self, task: Task):
        if "echo" in task.description.lower():
            return self.app.run_command("echo", **task.parameters)
        elif "add" in task.description.lower():
            return self.app.run_command("add_numbers", **task.parameters)
        elif "time" in task.description.lower() or "date" in task.description.lower():
            return self.app.run_command("get_datetime", **task.parameters)
        else:
            raise ValueError("No suitable command found.")
