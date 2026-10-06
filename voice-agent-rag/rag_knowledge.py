import os
import chromadb
from chromadb.utils import embedding_functions

# Lightweight local in-memory Chroma instance
chroma_client = chromadb.Client()
embedding_fn = embedding_functions.DefaultEmbeddingFunction()

collection = chroma_client.create_collection(
    name="company_faq", 
    embedding_function=embedding_fn
)

def ingest_faq():
    file_path = os.path.join(os.path.dirname(__file__), "data", "company_faq.txt")
    if not os.path.exists(file_path):
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split into sections based on double line breaks
    sections = [sec.strip() for sec in content.split("\n\n") if sec.strip()]
    ids = [f"faq_chunk_{i}" for i in range(len(sections))]
    
    collection.add(
        documents=sections,
        ids=ids
    )

# Run ingestion once when module is imported
ingest_faq()

def query_faq(question: str) -> str:
    """Queries the knowledge base for relevant facts."""
    results = collection.query(query_texts=[question], n_results=1)
    docs = results.get("documents", [[]])
    if docs and len(docs[0]) > 0:
        return docs[0][0]
    return "No matching policy found in the company manual."