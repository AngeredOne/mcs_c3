# agents/internal_improvement_agent.py

from core.agent import Agent
from core.task import Task


class InternalImprovementAgent(Agent):
    def __init__(self):
        super().__init__(name="internal_improvement_agent")
        self.role = "system_improver"

    def handle_task(self, task: Task):
        """
        Обрабатывает запросы на улучшение системы.
        Делегирует задачу агенту OpenAIAgent, который должен вернуть подробные рекомендации
        и варианты кода для улучшения системы.
        """
        # Формируем подробный запрос с описанием задачи и параметрами
        prompt = (
            f"System improvement request:\n"
            f"Description: {task.description}\n"
            f"Parameters: {task.parameters}\n\n"
            f"Provide detailed suggestions and complete code modifications if needed."
        )

        # Проверяем наличие агента OpenAIAgent
        if "openai_agent" not in self.app.agents:
            raise ValueError("OpenAIAgent is not available for system improvement.")

        openai_agent = self.app.agents["openai_agent"]

        # Создаем новую задачу для OpenAIAgent
        sub_task = Task(description=prompt, parameters={"prompt": prompt})

        # Делегируем задачу агенту OpenAIAgent
        result = openai_agent.handle_task(sub_task)

        # Сохраняем и возвращаем результат
        task.set_result(result)
        return result
