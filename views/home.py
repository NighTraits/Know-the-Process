import streamlit as st

from models import EROLE, IChat, KEY
from components import validation_message
from static.constants import DESCRIPTION, PROMPTS


def redirect_to_chat(prompt: str):
    st.session_state[KEY.CHAT_HISTORY].append(IChat(role=EROLE.USER, message=prompt))
    st.switch_page("views/chat.py")
    
def on_pill_change():
    value: str | None = st.session_state.get("action_pills")
    if value is not None:
        st.session_state["prompt_from_home"] = value
        st.session_state.action_pills = None

def page():    
    st.text("Bienvenido a")
    st.header("Know the Process PTY")
    
    
    with st.container(horizontal=False,width="content"):
        st.text(DESCRIPTION)
    
    
    # Options
    st.text("Preguntas")
    with st.container(horizontal=False,width="content", border=True):
        st.pills(
            " ",
            options=PROMPTS,
            key="action_pills",
            width=800,
            on_change=on_pill_change,
        )
        
        pending: str | None = st.session_state.pop("prompt_from_home", None)
        
        if pending is not None:
            validation_message(
                "¿ Deseas consultar la siguiente pregunta al agente?", 
                pending,
                redirect_to_chat,
            )
            

if __name__=="__main__":
    st.set_page_config(
        page_title="know the process",
        page_icon=":material/home:",
    )

    page()