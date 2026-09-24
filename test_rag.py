from app.rag import retrieve

results = retrieve(
    "What is GST Number?"
)

for i, doc in enumerate(results):

    print("\n")
    print("=" * 50)
    print(f"Result {i+1}")
    print("=" * 50)

    print(doc.page_content[:500])