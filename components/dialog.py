import streamlit as st
from typing import Callable

from uuid import uuid4

@st.dialog(" ", width="small", dismissible=False)
def pop_up_message(title: str, message: str)-> None:
    st.header(title, text_alignment="center")
    st.text(message, text_alignment="center", width="stretch")
    
    if st.button("Cerrar"):
        st.session_state["df_key"] = str(uuid4())
        st.rerun()
        
        
@st.dialog(" ", width="small")
def validation_message(
    title: str, 
    on_accept: Callable[[], None],
    message: str | None = "",
):
    st.subheader(title, text_alignment="center")
    st.text(message, text_alignment="center", width="stretch")
    
    with st.container(horizontal=True, width="stretch", horizontal_alignment="center"):
        if st.button("Cancelar"):
            st.rerun()
            
        if st.button("Aceptar"):
            on_accept()
            st.rerun()