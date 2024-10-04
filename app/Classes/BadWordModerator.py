import os
import re
from typing import Any, List
from .base_moderator import Moderator


class BadWordModerator(Moderator):
    def __init__(self):
        filepath = os.path.join(os.path.dirname(__file__), 'resource', 'stopWords.txt')
        with open(filepath, 'r', encoding='utf-8') as file:
            self.stop_words = [line.strip().lower() for line in file.readlines()]

    async def handle(self, request: Any, results: List[str]) -> List[str]:
        if isinstance(request, str):
            if self.filter_text(request):
                results.append('curse words')
        return await super().handle(request, results)

    def filter_text(self, text: str) -> bool:
        # Удаление пунктуации из текста
        text_without_punctuation = re.sub(r'[^\w\s]', ' ', text)
        words = text_without_punctuation.split()

        for word in words:
            if word.lower() in self.stop_words:
                return True
        return False
