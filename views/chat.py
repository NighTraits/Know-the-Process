import streamlit as st

from models import IChat, ROLE
from state import clear_chat_history
from services import prompt_agent

st.set_page_config(
    page_title="Chat",
    page_icon=":material/chat:",
)

# Header
with st.container(horizontal=True):
    st.title("Chat")
    st.button(
        label="limpiar historial",
        key="btn-clear-chat",
        on_click=clear_chat_history,
    )


# Chat history
for chat in st.session_state.chat_history:
    st.chat_message(chat.role).write(chat.message)


# Chat input box
if prompt := st.chat_input("Input your question here..."):
    st.chat_message(ROLE.USER).write(prompt)
    st.session_state.chat_history.append(IChat(role=ROLE.USER, message=prompt))


# Agent prompt with last message by user
if st.session_state.chat_history and (last_msg:=st.session_state.chat_history[-1]).role == ROLE.USER:
    response = prompt_agent(last_msg.message)
    st.session_state.chat_history.append(IChat(role=ROLE.ASSISTANT, message=response))
    st.rerun()