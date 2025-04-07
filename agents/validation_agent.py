# agents/validation_agent.py

from core.agent import Agent
from core.task import Task

class ValidationAgent(Agent):
    def __init__(self):
        super().__init__(name="validation_agent")
        self.role = "change_validator"

    def handle_task(self, task: Task):
        diff_text = task.parameters.get("diff")
        if not diff_text:
            raise ValueError("No diff available for validation.")

        print("\n=== Proposed Diff ===")
        print(diff_text)
        print("=====================\n")
        user_input = input("Apply this change? (yes/no): ").strip().lower()

        approved = user_input == "yes"
        task.parameters["approved"] = approved
        return {"approved": approved}
