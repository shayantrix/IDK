import opik
from core.config import settings
from langchain_openai import ChatOpenAI
from opik.integrations.langchain import OpikTracer

from core.rag.prompt_templates import QueryExpansionTemplate

class QueryExpansion:
    opik_tracer = OpikTracer(tags=["QueryExpansion"])

    @staticmethod
    @opik.track(name="QueryExpansion.generate_response")
    def generate_response(query: str, to_expand_to: int) -> list[str]:
        query_expansion_tempalte = QueryExpansionTemplate()
        prompt = query_expansion_tempalte.create_prompt_template(to_expand_to=5)
        model = ChatOpenAI(
            model=settings.OPENAI_MODEL_ID,
            api_key=settings.OPENAI_API_KEY,
            tempperature=0.0,
        )

        chain = prompt | model
        chain = chain.with_config({"callbacks": [QueryExpansion.opik_tracer]})

        response = chain.invoke({"question": query})
        response = response.content

        queries = response.strip().split(query_expansion_tempalte.seperator)

        stripped_queries = [
            stripped_items for item in queries if (stripped_items := item.strip(" \\n"))
        ]

        return stripped_queries