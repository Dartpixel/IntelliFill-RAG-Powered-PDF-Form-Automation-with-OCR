from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_core.documents import Document

from langchain_community.vectorstores import FAISS

from app.bedrock import embeddings
from app.pdf_utils import load_knowledge_base


KB_FOLDER = "data/knowledge_base"

VECTOR_PATH = "data/vector_store"


def create_vector_store():

    docs = load_knowledge_base(KB_FOLDER)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = []

    for doc in docs:

        split_docs = splitter.split_text(
            doc["content"]
        )

        for chunk in split_docs:

            chunks.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "source": doc["source"]
                    }
                )
            )

    vector_db = FAISS.from_documents(
        chunks,
        embeddings
    )

    vector_db.save_local(VECTOR_PATH)

    print("Vector DB Created")


def load_vector_store():

    return FAISS.load_local(
        VECTOR_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )


def retrieve(query, k=5, source=None):

    db = load_vector_store()

    search_kwargs = {"k": k}

    if source:
        search_kwargs["filter"] = {"source": source}

    return db.similarity_search(
        query,
        **search_kwargs
    )


def determine_primary_source(field_names, k=10):
    """
    Find which knowledge-base document is most relevant to a form's fields
    as a whole, so per-field retrieval can be restricted to that single
    source and avoid cross-document contamination. Individual field names
    are too short/generic to reliably match on their own, so they are
    combined into a single query representing the form's overall topic.
    """

    if not field_names:
        return None

    db = load_vector_store()

    query = " ".join(field_names)

    results = db.similarity_search(query, k=k)

    source_scores = {}

    for doc in results:
        source = doc.metadata.get("source")

        if not source:
            continue

        source_scores[source] = source_scores.get(source, 0) + 1

    if not source_scores:
        return None

    return max(source_scores, key=source_scores.get)