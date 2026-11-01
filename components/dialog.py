import streamlit as st

from uuid import uuid4

@st.dialog(" ", width="small", dismissible=False)
def pop_up_message(title: str, message: str)-> None:
    st.header(title, text_alignment="center")
    st.text(message, text_alignment="center", width="stretch")
    
    if st.button("Close"):
        st.session_state["df_key"] = str(uuid4())
        st.rerun()