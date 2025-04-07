# agents/logger_agent.py

from core.agent import Agent
from core.task import Task

class LoggerAgent(Agent):
    def __init__(self):
        super().__init__(name="logger_agent")
        self.role = "logger"

    def handle_task(self, task: Task):
        print(f"[LoggerAgent] Task: {task.description} | Params: {task.parameters}")
        return task
