from typing import Any, List
from .base_moderator import Moderator
import re


class EmailModerator(Moderator):
    async def handle(self, request: Any, results: List[str]) -> List[str]:
        if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', request):
            results.append('email addresses')
        return await super().handle(request, results)
