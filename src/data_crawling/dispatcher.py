import re

from .crawlers.base import BaseCrawler
from .crawlers.custom_article import CustomArticleCrawler


class CrawlerDispatcher:
    def __init__(self) -> None:
        self._crawlers = {}

    def register(self, pattern: str, crawler: type[BaseCrawler]) -> None:
        # Accept either a full regex pattern or a literal URL.
        if re.search(r"[\^\$\*\+\?\|\(\)\[\]\\]", pattern):
            compiled_pattern = pattern
        else:
            compiled_pattern = rf"^{re.escape(pattern)}$"
        self._crawlers[compiled_pattern] = crawler

    def get_crawler(self, url: str) -> BaseCrawler:
        for pattern, crawler in self._crawlers.items():
            if re.match(pattern, url):
                return crawler()
        else:
            print(f"No crawler registered for the given URL: {url}")

            return CustomArticleCrawler()
