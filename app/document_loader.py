
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader


def load_documents(folder_path: str = "data") -> list[Document]:
    """Load PDF and text files from a local folder."""
    folder = Path(folder_path)

    if not folder.is_dir():
        raise FileNotFoundError(f"Folder not found: {folder}")

    documents = []

    for file_path in sorted(folder.rglob("*")):
        if "vectorstore" in file_path.parts:
            continue
        if not file_path.is_file():
            continue

        if file_path.suffix.lower() == ".pdf":
            reader = PdfReader(str(file_path))

            for page_number, page in enumerate(reader.pages, start=1):
                content = page.extract_text()

                if content and content.strip():
                    documents.append(
                        Document(
                            page_content=content,
                            metadata={
                                "source": str(file_path),
                                "page": page_number,
                            },
                        )
                    )

        elif file_path.suffix.lower() in {".txt", ".md"}:
            content = file_path.read_text(encoding="utf-8")

            if content.strip():
                documents.append(
                    Document(
                        page_content=content,
                        metadata={"source": str(file_path)},
                    )
                )

    return documents


def split_documents(
    documents: list[Document],
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> list[Document]:
    """Split documents into overlapping text chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    return splitter.split_documents(documents)


if __name__ == "__main__":
    documents = load_documents()
    chunks = split_documents(documents)

    print(f"Documents loaded: {len(documents)}")
    print(f"Chunks created: {len(chunks)}")

    if chunks:
        print("\nFirst chunk preview:")
        print(chunks[0].page_content[:300])
