# agents/parameter_corrector_agent.py

from core.agent import Agent
from core.task import Task

class ParameterCorrectorAgent(Agent):
    def __init__(self):
        super().__init__(name="parameter_corrector_agent")
        self.role = "parameter_corrector"

    def handle_task(self, task: Task):
        corrected_params = {}
        for k, v in task.parameters.items():
            if isinstance(v, str):
                corrected_params[k] = v.strip()
            else:
                corrected_params[k] = v
        task.parameters = corrected_params
        return task
