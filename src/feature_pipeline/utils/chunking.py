from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    SentenceTransformersTokenTextSplitter,
)

from config import settings

def chunk_text(text: str) -> list[str]:
    character_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n"], chunk_size=500, chunk_overlap=0
    )
    text_split
