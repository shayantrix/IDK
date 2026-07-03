from abc import ABC, abstractmethod

from langchain.prompts import PromptTemplate
from pydantic import BaseModel

class BasePromptTemplate(ABC, BaseModel):
    @abstractmethod
    def create_prompt_template(self, *args) -> PromptTemplate:
        pass


class QueryExpansionTemplate(BasePromptTemplate):
    prompt: str = """You are called 'Alfered', and AI language model assistant. Your taks is to
    generate five different versions of the user's given question. 
    The generated questions should be semantically similar to the original question,
    but they should be phrased differently, to retrieve relevant documents from a vector database.
    By generating multiple perspectives on the user question, your goal is to help
    the user overcome some of the limitations of the distance-based similarity search. Provide these
    alternative questions seperated by '{separator}'.
    Original question: {query}""" 

    @property
    def seperator(self) -> str:
        return "#next-question#"

    def create_prompt_template(self, to_expand_to: int=5) -> PromptTemplate:
        return PromptTemplate(
            template=self.prompt,
            input_variables=["question"],
            partial_variables={
                "seperator": self.seperator,
                "to_expand_to": to_expand_to
            },
            verbose=True
        )
    

class SelfQueryTemplate(BasePromptTemplate):
    prompt: str = """You are called 'Alfered', and a AI Agent model assistant. Your task is to extract information from a user question.
    The required information that needs to be extracted is the name of the Document or the Book or author's name.
    Your response should consist of only the extracted author's name or document name, nothing else.
    If the user question does not contain any user name or id, you should return the following token: 'none'.
    
    For example:
    QUESTION 1:
    I want to answer this question '...' from this document called 'Reinforcement Learning An Introduction'...
    RESPONSE 1:
    Reinforcement Learning An Introduction
    
    QUESTION 2:
    what is the difference between this '...' and that '...' which both are mentioned in "Barto Sutton" Book about Reinforcement Learning...
    RESPONSE 2:
    Barto Sutton
    
    User question: {question}"""
    
    def create_prompt_template(self, *args) -> PromptTemplate:
        return PromptTemplate(
            template=self.prompt,
            input_variables=["question"],
            verbose=True
        )
    
class RerankingTemplate(BasePromptTemplate):
    prompt: str = """You are called 'Alfered', and a AI Agent model assistant. Your task is to rerank passages related to a query
    based on their relevance. 
    The most relevant passages should be put at the beginning. 
    You should only pick at max {keep_top_k} passages.
    The provided and reranked documents are separated by '{separator}'.
    
    The following are passages related to this query: {question}.
    
    Passages: 
    {passages}
    """

    def create_template(self, keep_top_k: int) -> PromptTemplate:
        return PromptTemplate(
            template=self.prompt,
            input_variables=["question", "passages"],
            partial_variables={
                "keep_top_k": keep_top_k,
                "separator": self.seperator,
            },
        )
    
    @property
    def seperator(self) -> str:
        return "\n#next-document#\n"

# hybrid score = (1 - alpha) * sparse_score + alpha * dense_score

# we can use keyword search algorithms too

# 
# we want the most relevant chunks from a given document or author name as folows
# 

# we have 2 strategies her: 
# 1- Simple vector-search-filter 
# 2- Hybrid search (vector+keyword) strategy
