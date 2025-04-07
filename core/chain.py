# core/chain.py

from typing import List, Any
from core.agent import Agent
from core.task import Task

class ProcessingChain:
    def __init__(self, name: str, agent_sequence: List[str]):
        self.name = name
        self.agent_sequence = agent_sequence

    def process(self, app: Any, task: Task) -> Task:
        for agent_name in self.agent_sequence:
            agent = app.agents.get(agent_name)
            if not agent:
                raise ValueError(f"Agent '{agent_name}' not found.")
            task = agent.handle_task(task)
        return task
