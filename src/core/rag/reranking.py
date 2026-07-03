from config import settings
from langchain_openai import ChatOpenAI

from core.rag.prompt_templates import RerankingTemplate

class Reranker:
    @staticmethod
    def generate_response(
        query: str, passages: list[str], keep_top_k: int
    ) -> list[str]:
        reranking_template = RerankingTemplate()
        prompt = reranking_template.create_template(keep_top_k=keep_top_k)
        model = ChatOpenAI(
            model=settings.OPENAI_MODEL_ID,
            api_key=settings.OPENAI_API_KEY,
        )

        chain = prompt | model
        response = chain.invoke({"question": query, "passages": passages})
        response = response.content

        reranked_passages = response.strip().split(reranking_template.seperator)

        stripped_passages = [
            stripped_items for item in reranked_passages if (stripped_items := item.strip(" \\n"))
        ]

        return stripped_passages