from app.rag import retrieve
from app.bedrock import llm


def generate_field_value(field_name, source=None):

    docs = retrieve(field_name, source=source)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
    You are a PDF form assistant.

    Field Name:
    {field_name}

    Context:
    {context}

    Rules:
    1. Return only the value.
    2. If not found return NOT_FOUND.
    3. No explanation.
    """

    response = llm.invoke(prompt)

    return response.content