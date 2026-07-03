from InstructorEmbedding import INSTRUCTOR
from sentence_transformers import SentenceTransformer

from core.config import settings
from feature_pipeline import word_counter


def embedd_text(text: str):
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    return model.encode(text)


def embedd_code(text: str):
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
        print(embedd_text(docs))
        print(embedd_code(docs))
