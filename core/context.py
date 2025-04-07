# core/context.py

from abc import ABC, abstractmethod
from typing import List, Tuple

class ContextStorage(ABC):
    @abstractmethod
    def add(self, text: str, metadata: dict) -> None:
        pass

    @abstractmethod
    def search(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        pass
