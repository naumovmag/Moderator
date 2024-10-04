from typing import Any, List
from .base_moderator import Moderator
import re


class LinkModerator(Moderator):
    excluded_domains = [
        'https://rabox.kz',
        'https://witches-empire.com',
        'https://womanisv.ru',
        'https://souz-isv.ru',
        'https://mama-i-deti.com',
        'https://joyisv.ru',
        'https://zdravnica-polin.com',
        'https://future-tv.ru',
        'https://femida-isv.com',
        'https://center-isv.com',
        'https://university-isv.com',
        'https://zdravnica-polin.com',
        'https://the-golden-calf.com',
        'https://kudesa-chudesa.com',
    ]

    async def handle(self, request: Any, results: List[str]) -> List[str]:
        if self.detect_links(request):
            results.append('links')
        return await super().handle(request, results)

    def detect_links(self, text: str) -> List[str]:
        pattern = r'((http|https|ftp):\/\/[^\s]+)'
        matches = re.findall(pattern, text)
        links = [match[0] for match in matches]

        for domain in self.excluded_domains:
            links = [link for link in links if not self.is_excluded_domain(link, domain)]

        return links

    @staticmethod
    def is_excluded_domain(link: str, domain: str) -> bool:
        parsed_link = re.search(r'^(?:http|https|ftp):\/\/([^\/]+)', link)
        parsed_domain = re.search(r'^(?:http|https|ftp):\/\/([^\/]+)', domain)

        if parsed_link and parsed_domain:
            return parsed_link.group(1) == parsed_domain.group(1)

        return False
