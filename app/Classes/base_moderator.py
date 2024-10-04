from abc import ABC, abstractmethod
from typing import Any, List


class Moderator(ABC):
    _next_handler = None

    def set_next(self, handler: 'Moderator') -> 'Moderator':
        self._next_handler = handler
        return handler

    @abstractmethod
    async def handle(self, request: Any, results: List[str]) -> List[str]:
        if self._next_handler:
            return await self._next_handler.handle(request, results)
        return results
