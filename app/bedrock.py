
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

from app.config import (
    OPENAI_API_KEY,
    OPENAI_MODEL_ID,
    OPENAI_EMBEDDING_MODEL_ID
)


llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    model=OPENAI_MODEL_ID
)

embeddings = OpenAIEmbeddings(
    api_key=OPENAI_API_KEY,
    model=OPENAI_EMBEDDING_MODEL_ID
)

