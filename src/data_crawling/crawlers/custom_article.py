import sys
from urllib.parse import urlparse

from core.db.documents import ArticleDocument
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import Html2TextTransformer


from bs4 import BeautifulSoup
import requests

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

        print("Hello world")
        loader = AsyncHtmlLoader([link], trust_env=True)
        docs = await loader.aload()
        print("Loaded docs: ", docs)
        print(26)

        docs[0].page_content[1000:2000]
        print(29)
        html2text = Html2TextTransformer()
        docs_transformed = html2text.transform_documents(docs)
        doc_transformed = docs_transformed[0]
        #
        print(doc_transformed)
        print(44)
        content = {
                    "Title": doc_transformed.metadata.get("title"),
                    "Subtitle": doc_transformed.metadata.get("description"),
                    "Content": doc_transformed.page_content,
                    "language": doc_transformed.metadata.get("language"),
                }

        print(52)

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
