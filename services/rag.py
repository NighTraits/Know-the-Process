import streamlit as st

from langchain.tools import tool
from langchain.agents import create_agent
from langchain_core.documents import Document
from langchain_chroma import Chroma, vectorstores
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_google_genai.chat_models import (
    GoogleAuthenticationError,
    GoogleInvalidRequestError,
    GoogleRateLimitError,
    GoogleAPIError,
)

from models.chat_schema import KEY


@st.cache_resource
def get_vectorstore() -> Chroma:
    embeddings = GoogleGenerativeAIEmbeddings(model=st.session_state[KEY.EMBEDDING])
    return Chroma(
        collection_name=st.session_state[KEY.COLLECTION],
        embedding_function=embeddings,
        persist_directory="./chroma_db",
    )

@st.cache_resource
def prompt_agent(question: str) -> str:    
    
    vector_store: vectorstores.Chroma = get_vectorstore()
    
    @tool
    def search_database(query: str) -> str:
        """Busca información, relevane al query, en el database"""
        results: list[Document] = vector_store.similarity_search(query, k=3)
        return "\n\n---\n\n".join(d.page_content for d in results) or "No results."
    
    
    model = ChatGoogleGenerativeAI(model=st.session_state[KEY.AGENT])
    
    agent = create_agent(
        model=model,
        tools=[search_database],
        system_prompt=(
            "Responde en español usando SOLO lo que se encuentra en el database."
            "Siempre usa la tool de busqueda en la database antes de responder."
            "Solo usa información recibida de la tool."
            "Si no se encuentra una respuesta, responde con no sé."
        ),
    )

    try:
        results = agent.invoke({"messages": question})
        return results["messages"][-1].text
    
    except GoogleInvalidRequestError as _:
        # HTTP Code 400
        return f"Ha surgido un problema con la consulta. Vuelva a intentarlo más tarde."
    
    except GoogleAuthenticationError as _:
        # HTTP Code 401
        return f"Ha surgido un problema con la clave. Consulte con los administradores sobre el caso."
    
    except GoogleRateLimitError as _:
        # HTTP Code 429
        return f"Límite de cuota alcanzada. Vuelva a intentarlo más tarde."
    
    except GoogleAPIError as _:
        # HTTP Code 5xx
        return f"Ha surgido un problema con los servidores. Vuelva a intentarlo más tarde."
    
    except Exception as _:
        # catch any other error not within the catched
        return f"Ha surgido un problema. Vuelva a intentarlo más tarde."