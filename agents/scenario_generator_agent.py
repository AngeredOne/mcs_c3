# agents/scenario_generator_agent.py

from core.agent import Agent
from core.task import Task
import uuid


class ScenarioGeneratorAgent(Agent):
    def __init__(self):
        super().__init__(name="scenario_generator_agent")
        self.role = "scenario_generator"

    def handle_task(self, task: Task):
        """
        Генерирует формальное описание сценария для решения специфичной задачи.
        Использует извлечённый контекст и передаёт запрос в OpenAIAgent для генерации деталей.
        """
        # Формируем базовый запрос
        prompt = (
            f"Generate a detailed scenario for the following task:\n"
            f"Description: {task.description}\n"
            f"Parameters: {task.parameters}\n"
            f"Ensure the scenario is a sequence of formal steps that determinize dynamic context into a clear sequence of instructions."
        )

        # Если контекст важен, можно дополнительно добавить последние сохранённые данные
        # Здесь можно реализовать извлечение релевантного контекста, если потребуется.
        # Пример: context = self.app.context.search(task.description)
        # prompt += f"\nRelevant context: {context}"

        # Проверяем наличие агента OpenAIAgent
        if "openai_agent" not in self.app.agents:
            raise ValueError("OpenAIAgent is not available for scenario generation.")

        openai_agent = self.app.agents["openai_agent"]
        sub_task = Task(description=prompt, parameters={"prompt": prompt})

        # Делегируем генерацию сценария агенту OpenAIAgent
        generated_response = openai_agent.handle_task(sub_task)

        # Предполагаем, что полученный ответ – это текст с описанием сценария,
        # который можно разобрать на шаги. Здесь приведён базовый пример:
        steps = {}
        # Разбиваем полученный ответ по строкам и создаём шаги с уникальными именами.
        for line in generated_response.get("response", "").splitlines():
            if line.strip():
                step_id = f"step_{uuid.uuid4().hex}"
                # В данном примере не проводится глубокий разбор, но можно расширить логику.
                steps[step_id] = {
                    "instruction": line.strip()
                }

        # Формируем итоговый сценарий как словарь
        scenario = {
            "name": f"generated_scenario_{uuid.uuid4().hex}",
            "steps": steps
        }

        task.set_result(scenario)
        return scenario
