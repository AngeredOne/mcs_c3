# agents/goal_validator_agent.py

from core.agent import Agent
from core.task import Task

class GoalValidatorAgent(Agent):
    def __init__(self):
        super().__init__(name="goal_validator_agent")
        self.role = "validator"

    def handle_task(self, task: Task):
        if not task.description or len(task.description.strip()) < 5:
            raise ValueError("Task description is too short or unclear.")
        return task
