# core/llm_agent_interface.py

from abc import ABC, abstractmethod

class LLMAgentInterface(ABC):
    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        """Должен вернуть ответ на запрос."""
        pass

class ExtendedLLMAgentInterface(LLMAgentInterface):
    @abstractmethod
    def chat(self, system_prompt: str, messages: list, temperature: float = 0.7) -> str:
        """Supports full chat context: system prompt, history, temperature."""
        pass
