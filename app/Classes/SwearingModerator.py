import os
from typing import Any, List
import re
from .base_moderator import Moderator


class SwearingModerator(Moderator):
    def __init__(self):
        filepath = os.path.join(os.path.dirname(__file__), 'resource', 'swearingWords.txt')
        with open(filepath, 'r', encoding='utf-8') as file:
            self.stop_words = [line.strip().lower() for line in file.readlines()]

    async def handle(self, request: Any, results: List[str]) -> List[str]:
        if isinstance(request, str):
            if self.contains_swearing(request):
                results.append('swearing')
        return await super().handle(request, results)

    def contains_swearing(self, text: str) -> bool:
        for stop_word in self.stop_words:
            pattern = re.compile(re.escape(stop_word), re.IGNORECASE)
            if pattern.search(text):
                return True
        return False
