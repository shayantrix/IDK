import re

from .crawlers.base import BaseCrawler
from .crawlers.custom_article import CustomArticleCrawler


class CrawlerDispatcher:
    def __init__(self) -> None:
        self._crawlers = {}

    def register(self, domain: str, crawler: type[BaseCrawler]) -> None:
        self._crawlers[r"https://(www\.)?{}.com/*".format(re.escape(domain))] = crawler

    def get_crawler(self, url: str) -> BaseCrawler:
        for pattern, crawler in self._crawlers.items():
            if re.match(pattern, url):
                return crawler()
        else:
            print(f"No crawler registered for the given URL: {url}")

            return CustomArticleCrawler()
