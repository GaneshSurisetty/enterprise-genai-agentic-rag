
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from app.document_loader import load_documents, split_documents


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
INDEX_PATH = "data/vectorstore"


def create_embeddings():
    return HuggingFaceEmbeddings(
        model_name=MODEL_NAME,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def build_vectorstore():
    documents = load_documents("data")
    chunks = split_documents(documents)

    if not chunks:
        raise ValueError("No document chunks found in data folder.")

    embeddings = create_embeddings()

    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings,
    )

    Path(INDEX_PATH).mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(INDEX_PATH)

    return vectorstore, len(chunks)


if __name__ == "__main__":
    vectorstore, count = build_vectorstore()

    print(f"Successfully indexed {count} document chunks.")

    question = "What technology is used for semantic search?"

    results = vectorstore.similarity_search(question, k=2)

    print(f"\nQuestion: {question}")

    for i, document in enumerate(results, start=1):
        print(f"\nResult {i}:")
        print(f"Source: {document.metadata.get('source')}")
        print(document.page_content[:400])
