import json

from core.config import settings

MAX_LENGTH = 16384
SYSTEM_PROMPT = (
    "You are a technical Network programming assistant that knows the code and answers to different solutions for os network programming"
)

class LLMCommunicator:
    def __init__(self, llm_model: str = settings.)
