from dotenv import load_dotenv
import os

# encoding="utf-8-sig" tolerates a UTF-8 BOM (editors on Windows often add one),
# which otherwise breaks the first key (e.g. AWS_REGION becomes \ufeffAWS_REGION).
load_dotenv(override=True, encoding="utf-8-sig")


AWS_REGION = os.getenv("AWS_REGION")

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")

AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

MODEL_ID = os.getenv("MODEL_ID")

EMBEDDING_MODEL_ID = os.getenv(
    "EMBEDDING_MODEL_ID"
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

OPENAI_MODEL_ID = os.getenv("OPENAI_MODEL_ID", "gpt-4o-mini")

OPENAI_EMBEDDING_MODEL_ID = os.getenv(
    "OPENAI_EMBEDDING_MODEL_ID", "text-embedding-3-small"
)