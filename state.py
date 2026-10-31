from uuid import uuid4
from services import get_data
import streamlit as st


# def save_data(data: IContent) -> None:
#     STORE.write_text(json.dumps(data, indent=4, default=str))


# def update_data(key: str, value: str) -> None:
#     st.session_state.data[key] = value
#     save_data(st.session_state.data)


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

    if "rag" not in st.session_state:
        st.session_state.rag = True
        
    if "df_key" not in st.session_state:
        st.session_state.df_key = str(uuid4())