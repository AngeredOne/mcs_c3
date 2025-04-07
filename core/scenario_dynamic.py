# core/scenario_dynamic.py

from typing import Dict, Optional
from core.task import Task

from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from core.app import CoreApp


class ScenarioStep:
    def __init__(self, name: str, chain_name: Optional[str], required_role: str,
                 next_step_on_success: Optional[str] = None,
                 next_step_on_failure: Optional[str] = None):
        self.name = name
        self.chain_name = chain_name
        self.required_role = required_role
        self.next_step_on_success = next_step_on_success
        self.next_step_on_failure = next_step_on_failure

class Scenario:
    def __init__(self, name: str, steps: Dict[str, ScenarioStep], start_step: str):
        self.name = name
        self.steps = steps
        self.start_step = start_step

class StepModification:
    def __init__(self, add_steps: Optional[Dict[str, ScenarioStep]] = None,
                 override_next_step: Optional[str] = None):
        self.add_steps = add_steps or {}
        self.override_next_step = override_next_step

class ScenarioExecutor:
    def __init__(self, app: "CoreApp", session_id: str):
        self.app = app
        self.session_id = session_id

    def execute(self, scenario: Scenario, task: Task) -> Dict[str, Any]:
        current_step_name = scenario.start_step
        history = []

        result = None

        while current_step_name:
            step = scenario.steps[current_step_name]
            agent = self.find_agent_by_role(step.required_role)
            if not agent:
                raise Exception(f"No agent found with role '{step.required_role}'")

            try:
                if step.chain_name:
                    task = self.app.process_task_via_chain(step.chain_name, task)

                result = agent.handle_task(task)
                task.add_role_history(role=step.required_role, agent=agent.name)

                modification = None
                if isinstance(result, tuple) and len(result) == 2:
                    result, modification = result

                if modification:
                    if modification.add_steps:
                        scenario.steps.update(modification.add_steps)
                    if modification.override_next_step:
                        current_step_name = modification.override_next_step
                        continue

                history.append({
                    "step": current_step_name,
                    "agent": agent.name,
                    "result": str(result),
                    "status": "success"
                })

                current_step_name = step.next_step_on_success
            except Exception as e:
                history.append({
                    "step": current_step_name,
                    "agent": agent.name,
                    "error": str(e),
                    "status": "failure"
                })
                current_step_name = step.next_step_on_failure

        task.set_result(result)
        return {
            "task_final_state": task,
            "execution_history": history
        }

    def find_agent_by_role(self, role: str):
        for agent in self.app.agents.values():
            if getattr(agent, "role", None) == role:
                return agent
        return None
