# agents/planner_agent.py

from core.agent import Agent
from core.task import Task

class PlannerAgent(Agent):
    def __init__(self):
        super().__init__(name="planner_agent")
        self.role = "planner"

    def handle_task(self, task: Task):
        subtasks = self._decompose(task.description)
        results = []
        for subdesc in subtasks:
            subtask = Task(description=subdesc, parameters=task.parameters.copy())
            result = self.app.delegate_task("default", "simple_task_agent", subtask)
            results.append((subdesc, result))
        return {"original": task.description, "subtasks": results}

    def _decompose(self, goal: str):
        if "and" in goal:
            return [part.strip() for part in goal.split("and")]
        return [goal.strip()]
