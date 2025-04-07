# agents/task_planner_agent.py

from core.agent import Agent
from core.task import Task
from core.scenario_dynamic import Scenario, ScenarioStep
import uuid

class TaskPlannerAgent(Agent):
    def __init__(self):
        super().__init__(name="task_planner_agent")
        self.role = "task_planner"

    def handle_task(self, task: Task):
        description = task.description.lower()

        # Простейшая эвристика для планирования (можно усложнить через LLM)
        steps = {}
        start_step = None

        if "refactor" in description or "extract" in description:
            # Шаг 1: Чтение файла
            read_step = f"read_{uuid.uuid4().hex}"
            steps[read_step] = ScenarioStep(
                name=read_step,
                chain_name=None,
                required_role="filesystem_operator",
                next_step_on_success=None  # Будет заполнено позже
            )
            start_step = read_step

            # Шаг 2: Разработка изменения
            dev_step = f"develop_{uuid.uuid4().hex}"
            steps[dev_step] = ScenarioStep(
                name=dev_step,
                chain_name=None,
                required_role="inner_developer",
                next_step_on_success=None
            )
            steps[read_step].next_step_on_success = dev_step

            # Шаг 3: Создание диффа
            diff_step = f"diff_{uuid.uuid4().hex}"
            steps[diff_step] = ScenarioStep(
                name=diff_step,
                chain_name=None,
                required_role="filesystem_operator",
                next_step_on_success=None
            )
            steps[dev_step].next_step_on_success = diff_step

            # Шаг 4: Валидация изменений
            validate_step = f"validate_{uuid.uuid4().hex}"
            steps[validate_step] = ScenarioStep(
                name=validate_step,
                chain_name=None,
                required_role="change_validator",
                next_step_on_success=None
            )
            steps[diff_step].next_step_on_success = validate_step

            # Шаг 5: Применение изменений
            apply_step = f"apply_{uuid.uuid4().hex}"
            steps[apply_step] = ScenarioStep(
                name=apply_step,
                chain_name=None,
                required_role="filesystem_operator",
                next_step_on_success=None
            )
            steps[validate_step].next_step_on_success = apply_step
        else:
            raise ValueError("Planner does not know how to handle this type of task yet.")

        # Создание динамического сценария
        scenario = Scenario(
            name=f"dynamic_{uuid.uuid4().hex}",
            steps=steps,
            start_step=start_step
        )

        # Регистрация сценария на лету
        self.app.register_scenario(scenario)

        return {"scenario_name": scenario.name}