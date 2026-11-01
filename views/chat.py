import streamlit as st

from models import IChat, EROLE, KEY
from state import clear_chat_history
from services import prompt_agent


def page():
    with st.container(horizontal=True, horizontal_alignment="right"):
        st.button(
            label="limpiar historial",
            key="btn-clear-chat",
            on_click=clear_chat_history,
        )

    # Chat history
    for chat in st.session_state[KEY.CHAT_HISTORY]:
        st.chat_message(chat.role).write(chat.message)


    # Chat input box
    if prompt := st.chat_input("Input your question here..."):
        st.chat_message(EROLE.USER).write(prompt)
        st.session_state[KEY.CHAT_HISTORY].append(IChat(role=EROLE.USER, message=prompt))


    # Agent prompt with last message by user
    if st.session_state[KEY.CHAT_HISTORY] and (last_msg:=st.session_state[KEY.CHAT_HISTORY][-1]).role == EROLE.USER:
        response = prompt_agent(last_msg.message)
        st.session_state[KEY.CHAT_HISTORY].append(IChat(role=EROLE.ASSISTANT, message=response))
        st.rerun()
        
    
if __name__=="__main__":
    st.set_page_config(page_title="Chat", page_icon=":material/chat:")
    st.title("Chat")
    
    requirements = [
        KEY.EMBEDDING,
        KEY.AGENT,
        KEY.COLLECTION,
    ]
    
    if not all([r in st.session_state for r in requirements]) or KEY.API_KEY not in st.secrets:
        st.error("Agente no disponible.")
        st.stop()
    
    page()