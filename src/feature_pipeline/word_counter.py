import re

from core.db.documents import ArticleDocument


def get_article_content(article_id: str) -> str:
    article = ArticleDocument.find(_id=article_id)
    if article is None:
        raise ValueError(f"Article not found for id={article_id}")

    content = article.content if isinstance(article.content, dict) else {}
    return str(content.get("Content", ""))


def count_words(text: str) -> int:
    return len(re.findall(r"\S+", text))


if __name__ == "__main__":
    article_id = "4b137f52-e3f2-4bfa-87e3-9505cefe1375"
    text = get_article_content(article_id)
    print(text)
    print(count_words(text))
