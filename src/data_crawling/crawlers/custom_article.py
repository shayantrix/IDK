import os
from urllib.parse import urlparse

# LangChain checks USER_AGENT while loading some components.
os.environ.setdefault(
    "USER_AGENT",
    "idk-crawler/0.1 (+https://beej.us/guide/bgnet/html/index-wide.html)",
)

from core.db.documents import ArticleDocument
from langchain_community.document_loaders import AsyncHtmlLoader
from bs4 import BeautifulSoup

from .base import BaseCrawler

class CustomArticleCrawler(BaseCrawler):
    model = ArticleDocument

    def __init__(self) -> None:
        super().__init__()

    async def extract(self, link: str, **kwargs) -> None:
        old_model = self.model.find(link=link)
        if old_model is not None:
            print(f"Article already exists: {link}")
            return

        print(f"Starting scrapping article.....: {link}")

        # response = requests.get(link)
        # docs = BeautifulSoup(response.text, 'html.parser')
        # doc_transformed = docs.get_text()

        loader = AsyncHtmlLoader([link], trust_env=True)
        docs = await loader.aload()
        try:
            from langchain_community.document_transformers import Html2TextTransformer

            html2text = Html2TextTransformer()
            docs_transformed = html2text.transform_documents(docs)
            doc_transformed = docs_transformed[0]
            page_content = doc_transformed.page_content
            metadata = doc_transformed.metadata
        except Exception:
            soup = BeautifulSoup(docs[0].page_content, "html.parser")
            page_content = soup.get_text(separator="\n", strip=True)
            metadata = docs[0].metadata

        content = {
                    "Title": metadata.get("title"),
                    "Subtitle": metadata.get("description"),
                    "Content": page_content,
                    "language": metadata.get("language"),
                }

        parsed_url = urlparse(link)
        platform = parsed_url.netloc
        # platform is the same as domain name

        instance = self.model(
            content=content,
            link=link,
            platform=platform,
            author_id=kwargs.get("author_id"),
        )
        document_id = instance.save()
        print(f"Finished scrapping article: {link}")
        print(f"Inserted Id of the document: {document_id}")
