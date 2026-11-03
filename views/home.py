import streamlit as st

from pydantic import TypeAdapter
from functools import partial

from models import EROLE, IChat, KEY
from components import validation_message
from models.data_schema import IContent
from static.constants import DESCRIPTION, PROMPTS


def redirect_to_chat(prompt: str):
    st.session_state[KEY.CHAT_HISTORY].append(IChat(role=EROLE.USER, message=prompt))
    st.switch_page("views/chat.py")


def redirect_to_archive(location: str):
    st.switch_page("views/archive.py", query_params=[("locationId", location)])

# Prompt selection handler. Trigger and close dialog.
def on_pill_change(pill_key: str, val_key: str):
    value: str | None = st.session_state.get(pill_key)
    if value is not None:
        st.session_state[val_key] = value
        st.session_state[pill_key] = None


def page():    
    with st.container(horizontal=True):
        
        # Title section
        with st.container(horizontal=False):
            st.text("Bienvenido a")
            with st.container(horizontal=True, horizontal_alignment="left", width="content", vertical_alignment="bottom", gap=0):
                st.header("Know the Process PTY")
                st.text("ver.1.0.0")
            st.text(DESCRIPTION)
           
        # Prompt options
        with st.container(horizontal=False, width="stretch", border=True):
            st.pills(
                "Prueba el agente con las siguientes preguntas:",
                options=PROMPTS,
                key="prompt_pills",
                on_change=on_pill_change("prompt_pills", "prompt_from_home"),
            )
            if (prompt:=st.session_state.pop("prompt_from_home", None)):
                validation_message(
                    title="¿Deseas consultar la siguiente pregunta al agente?", 
                    message=prompt,
                    on_accept=partial(redirect_to_chat, prompt),
                )
    # All locations list
    with st.container(horizontal=False, width="content", border=True):
        if not (data:=st.session_state[KEY.DATA]):
            st.stop()
        data = TypeAdapter(list[IContent]).validate_python(data)
        options = set([dt.location for dt in data])
        if (location_id:=st.pills(
            "Instituciones",
            options=options,
        )):
            redirect_to_archive(location_id)
            

if __name__=="__main__":
    st.set_page_config(
        page_title="know the process",
        page_icon=":material/home:",
    )

    page()