import json
from pathlib import Path
import streamlit as st
from models.data_schema import IContent

STORE = Path("static/db.json")


def load_data() -> dict[str, str]:
    return json.loads(STORE.read_text()) if STORE.exists() else {}


def save_data(data: IContent) -> None:
    STORE.write_text(json.dumps(data, indent=4, default=str))


def update_data(key: str, value: str) -> None:
    st.session_state.data[key] = value
    save_data(st.session_state.data)


def clear_chat_history() -> None:
    st.session_state.chat_history = []


def init_state() -> None:
    if "chat_history" not in st.session_state:
        clear_chat_history()

    if "data" not in st.session_state:
        st.session_state.data = load_data()
