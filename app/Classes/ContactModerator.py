from typing import Any, List
import re
from .base_moderator import Moderator


class ContactModerator(Moderator):
    async def handle(self, request: Any, results: List[str]) -> List[str]:
        if isinstance(request, str) and self.detect_phone_numbers(request):
            results.append('phone numbers')
        return await super().handle(request, results)

    @staticmethod
    def detect_phone_numbers(text):
        patterns = [
            r'[\+]?([7|8])[-|\s]?\([-|\s]?(\d{3})[-|\s]?\)[-|\s]?(\d{3})[-|\s]?(\d{2})[-|\s]?(\d{2})',
            r'[\+]?([7|8])[-|\s]?(\d{3})[-|\s]?(\d{3})[-|\s]?(\d{2})[-|\s]?(\d{2})',
            r'[\+]?([7|8])[-|\s]?\([-|\s]?(\d{4})[-|\s]?\)[-|\s]?(\d{2})[-|\s]?(\d{2})[-|\s]?(\d{2})',
            r'[\+]?([7|8])[-|\s]?(\d{4})[-|\s]?(\d{2})[-|\s]?(\d{2})[-|\s]?(\d{2})',
            r'[\+]?([7|8])[-|\s]?\([-|\s]?(\d{4})[-|\s]?\)[-|\s]?(\d{3})[-|\s]?(\d{3})',
            r'[\+]?([7|8])[-|\s]?(\d{4})[-|\s]?(\d{3})[-|\s]?(\d{3})',
        ]

        phone_numbers = []

        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                phone_numbers.extend(matches)

        return phone_numbers
