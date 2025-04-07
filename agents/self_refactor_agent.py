# agents/self_refactor_agent.py

from core.agent import Agent
from core.task import Task

class SelfRefactorAgent(Agent):
    def __init__(self):
        super().__init__(name="self_refactor_agent")
        self.role = "self_refactor"

    def handle_task(self, task: Task):
        suggestions = []

        # Анализ именования агентов
        suggestions.append("Проверьте единообразие имен агентов для повышения читаемости кода.")

        # Анализ обработки ошибок
        suggestions.append("Рассмотрите централизованную обработку ошибок и логирование в ScenarioExecutor.")

        # Анализ динамических сценариев
        suggestions.append("Подумайте о вынесении генерации сценариев в отдельный модуль для упрощения расширяемости.")

        # Анализ использования LLM
        suggestions.append("Добавьте обработку отсутствия API-ключа для OpenAIAgent с подробными сообщениями об ошибке.")

        task.set_result({"suggestions": suggestions})
        return {"suggestions": suggestions}
