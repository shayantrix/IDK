from pathlib import Path
import sys
from typing import Any
import asyncio

# Allow running this file directly: `python src/data_crawling/main.py`
PROJECT_SRC = Path(__file__).resolve().parents[1]
if str(PROJECT_SRC) not in sys.path:
    sys.path.insert(0, str(PROJECT_SRC))

from .dispatcher import CrawlerDispatcher
from .crawlers.custom_article import CustomArticleCrawler

_dispatcher = CrawlerDispatcher()
_dispatcher.register("https://beej.us/guide/bgnet/html/index-wide.html", CustomArticleCrawler)

async def handler(event) -> dict[str, Any]:
    link = event.get("link")
    user_id = event.get("user")
    crawler = _dispatcher.get_crawler(link)

    try:
        await crawler.extract(link=link, author_id=user_id)
        return {
            "statuscode": 200, "body": "Link processed successfully"
        }
    except Exception as e:
        return {
            "statuscode": 500, "body": f"An error occurred: {str(e)}"
        }


if __name__ == "__main__":
    event = {
        "user": "Beej Jorgensen",
        "link": "https://beej.us/guide/bgnet/html/index-wide.html",
    }

    result = asyncio.run(handler(event))
    print(result)
