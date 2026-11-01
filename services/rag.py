import streamlit as st

from langchain.tools import tool
from langchain.agents import create_agent
from langchain_core.documents import Document
from langchain_chroma import Chroma, vectorstores
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

@st.cache_resource
def get_vectorstore() -> Chroma:
    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
    return Chroma(
        collection_name=st.secrets["COLLECTION"],
        embedding_function=embeddings,
        persist_directory="./chroma_db",
    )

@st.cache_resource
def prompt_agent(question: str) -> str:    
    
    vector_store: vectorstores.Chroma = get_vectorstore()
    
    @tool
    def search_database(query: str) -> str:
        """Search the database for records relevant to the query."""
        results: list[Document] = vector_store.similarity_search(query, k=3)
        return "\n\n---\n\n".join(d.page_content for d in results) or "No results."

    
    model = ChatGoogleGenerativeAI(model=st.secrets["CHAT_MODEL"])
    
    agent = create_agent(
        model=model,
        tools=[search_database],
        system_prompt=(
            "Responde en español usando SOLO lo que se encuentra en el database."
            "Siempre usa la tool de busqueda en la database antes de responder."
            "Solo usa información recibida de la tool."
            "Si no se encuentra una respuesta, di que no sabes."
        ),
    )

    try:        
        results = agent.invoke({"messages": question})
        return results["messages"][-1].text
    
    except Exception as e:
        st.toast(f"{e}", icon=":material/error:")
        return ""