import asyncio

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    SentenceTransformersTokenTextSplitter,
)

from core.config import settings
from feature_pipeline import word_counter


def chunk_text(text: str) -> list[str]:
    character_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)

    text_split = character_splitter.split_text(text)

    token_splitter = SentenceTransformersTokenTextSplitter(
        chunk_overlap=50,
        tokens_per_chunk=settings.EMBEDDING_MODEL_MAX_INPUT_LENGTH,
        model_name=settings.EMBEDDING_MODEL,
    )

    chunks = []
    for section in text_split:
        chunks.extend(token_splitter.split_text(section))

    return chunks


if __name__ == "__main__":
    article_ids = word_counter.list_article_ids()
    if not article_ids:
        print("No articles found.")
    else:
        article_id = word_counter.choose_article_id(article_ids)
        docs = word_counter.get_article_content(article_id)
        chunks = chunk_text(docs)
        print(f"Chunked {len(chunks)} sections.")
        print(chunks[1:25])
