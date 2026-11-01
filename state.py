from uuid import uuid4
from services import get_data
import streamlit as st
import os

def clear_chat_history() -> None:
    st.session_state.chat_history = []


def init_state() -> None:
    if "chat_history" not in st.session_state:
        clear_chat_history()

    if "data" not in st.session_state:
        data = get_data()
        if not data:
            st.toast("Error de carga de datos.", icon=":material/error:")
        st.session_state.data = data
        
    if "df_key" not in st.session_state:
        st.session_state.df_key = str(uuid4())
        
    if not os.environ.get("GOOGLE_API_KEY"):
        if not (key:=st.secrets["GOOGLE_API_KEY"]):
            st.toast("No se encontró al clave de Gemini.", icon="/material:error/")
        else:
            os.environ["GOOGLE_API_KEY"] = key
