from urllib.parse import urlparse

from core.db.documents import ArticleDocument
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import Html2TextTransformer

from .base import BaseCrawler

class CustomArticleCrawler(BaseCrawler):
    model = Article
