import os
import json
from time import sleep
from dotenv import load_dotenv
from pathlib import Path

from langchain_core.documents.base import Document
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv(".streamlit/secrets.toml")

def load_documents(path: Path) -> list[Document]:
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    
    docs: list[Document] = []
    for rec in data:
        text: str = "\n".join(f"{k}: {v}" for k, v in rec.items())
        
        meta: dict[str,str] = {k: str(v) for k, v in rec.items()}
        meta["record_id"] = rec['id']
        
        docs.append(Document(page_content=text, metadata=meta))
        
    return docs


def create_chroma() -> None:
    """
        Store db.json data in a chroma vector, to be used by the model.
    """
    model: str = os.getenv("EMBEDDING_MODEL") or ""
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY") or ""
    collection_name = os.getenv("COLLECTION") or ""
    
    embeddings = GoogleGenerativeAIEmbeddings(model=model)
    docs: list[Document] = load_documents(Path("static/db.json"))
    
    vector_store = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory="./chroma_db"
    )
    
    for i in range(0, len(docs), 5):
        vector_store.add_documents(
            documents=docs[i:i+5],
            ids=[str(d.metadata["record_id"]) for d in docs[i:i+5]]
        )
        # wait for embedding tokens to restart (1 minute)
        if i > 0 and i % 50 == 0:
            sleep(60)
    
if __name__ == "__main__":
    create_chroma()