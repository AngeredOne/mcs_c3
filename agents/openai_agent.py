# agents/openai_agent.py

from core.agent import Agent
from core.task import Task
from core.llm_agent_interface import ExtendedLLMAgentInterface
import openai
import os


class OpenAIAgent(Agent, ExtendedLLMAgentInterface):
    def __init__(self, model: str = "gpt-4", temperature: float = 0.2):
        super().__init__(name="openai_agent")
        self.role = "external_llm"
        self.model = model
        self.temperature = temperature
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def generate_response(self, prompt: str) -> str:
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature
        )
        return response.choices[0].message.content.strip()

    def chat(self, system_prompt: str, messages: list, temperature: float = 0.7) -> str:
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")

        full_messages = [{"role": "system", "content": system_prompt}] + messages

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=full_messages,
            temperature=temperature
        )
        return response.choices[0].message.content.strip()

    def handle_task(self, task: Task):
        if "messages" in task.parameters and "system_prompt" in task.parameters:
            result = self.chat(
                system_prompt=task.parameters["system_prompt"],
                messages=task.parameters["messages"],
                temperature=task.parameters.get("temperature", self.temperature)
            )
        elif "prompt" in task.parameters:
            result = self.generate_response(task.parameters["prompt"])
        else:
            raise ValueError("Task must contain either 'prompt' or ('system_prompt' + 'messages').")

        task.set_result(result)
        return {"response": result}
