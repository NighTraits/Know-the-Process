import streamlit as st

import os

from models import KEY
from services import get_data
from static.constants import AGENT_MODEL, EMBEDDING_MODEL, COLLECTION


def clear_chat_history() -> None:
    st.session_state[KEY.CHAT_HISTORY] = []


def init_state() -> None:
    if not os.environ.get(KEY.GOOGLE_API_KEY):
        try:
            os.environ[KEY.GOOGLE_API_KEY] = st.secrets[KEY.API_KEY]
        except Exception:
            st.error("No se encontró al clave de Gemini.", icon=":material/error:")

    if KEY.EMBEDDING not in st.session_state:
        try:
            st.session_state[KEY.EMBEDDING] = EMBEDDING_MODEL
        except Exception:
            st.error("No se encontró especificación del modelo de embedding.", icon=":material/error:")            

    if KEY.AGENT not in st.session_state:
        try:
            st.session_state[KEY.AGENT] = AGENT_MODEL
        except Exception:
            st.error("No se encontró especificación del modelo del agente.", icon=":material/error:")

    if KEY.COLLECTION not in st.session_state:
        try:
            st.session_state[KEY.COLLECTION] = COLLECTION
        except Exception:
            st.error("No se encontró el nombre de la colección la base de datos.", icon=":material/error:")
            
    if KEY.CHAT_HISTORY not in st.session_state:
        clear_chat_history()

    if KEY.DATA not in st.session_state:
        data = get_data()
        if not data:
            st.error("Error de carga de datos.", icon=":material/error:")
        st.session_state[KEY.DATA] = data
        