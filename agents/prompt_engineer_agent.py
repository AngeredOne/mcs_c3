# agents/prompt_engineer_agent.py

from core.agent import Agent
from core.task import Task

class PromptEngineerAgent(Agent):
    def __init__(self):
        super().__init__(name="prompt_engineer_agent")
        self.role = "prompt_engineering"

    def handle_task(self, task: Task):
        task.description = f"Refined Task: {task.description.strip().capitalize()}"
        return task
