from abc import ABC, abstractmethod

from models.base import DataModel
from models.clean import ArticleCleanedModel
from models.raw import ArticleRawModel
from utils.cleaning import clean_text
