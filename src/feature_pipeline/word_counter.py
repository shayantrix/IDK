import re

from core.db.documents import ArticleDocument
from core.db.mongo import connection


def list_article_ids() -> list[str]:
    db = connection.get_database()
    collection = db[ArticleDocument.Settings.name]
    ids = [str(doc.get("_id")) for doc in collection.find({}, {"_id": 1}) if doc.get("_id")]
    return ids


def get_article_content(article_id: str) -> str:
    article = ArticleDocument.find(_id=article_id)
    if article is None:
        raise ValueError(f"Article not found for id={article_id}")

    content = article.content if isinstance(article.content, dict) else {}
    return str(content.get("Content", ""))


def count_words(text: str) -> int:
    return len(re.findall(r"\S+", text))


def choose_article_id(ids: list[str]) -> str:
    print("Available article IDs:")
    for index, article_id in enumerate(ids, start=1):
        print(f"{index}. {article_id}")

    while True:
        selected = input("Choose article number: ").strip()
        if selected.isdigit():
            position = int(selected)
            if 1 <= position <= len(ids):
                return ids[position - 1]
        print("Invalid selection. Please enter a valid number.")


if __name__ == "__main__":
    article_ids = list_article_ids()
    if not article_ids:
        print("No articles found.")
    else:
        article_id = choose_article_id(article_ids)
        text = get_article_content(article_id)
        print("\nSelected article id:", article_id)
        print("\nContent:\n")
        print(text)
        print("\nWord count:", count_words(text))
