from InstructorEmbedding import INSTRUCTOR
from sentence_transformers import SentenceTransformer

from core.config import settings
from feature_pipeline import word_counter


def embedded_text(text: str):
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    return model.encode(text)


def embedded_repositories(text: str):
    model = INSTRUCTOR("hkunlp/instructor-xl")
    instruction = "Represent the structure of the repository"

    return model.encode([instruction, text])


if __name__ == "__main__":
    article_ids = word_counter.list_article_ids()
    if not article_ids:
        print("No articles found.")
    else:
        article_id = word_counter.choose_article_id(article_ids)
        docs = word_counter.get_article_content(article_id)
        print(embedded_text(docs))
        print(embedded_repositories(docs))
