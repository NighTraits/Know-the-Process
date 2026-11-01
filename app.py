import streamlit as st

from state import init_state
from streamlit.navigation.page import Page

st.set_page_config(
    page_title="Know the Process",
    layout="wide"
)
st.logo("static/logo.svg", size="large")

# load session state
init_state()

# Router
pages: list[Page] = [
    st.Page("views/home.py", title="Home", icon=":material/home:", default=True),
    st.Page("views/chat.py", title="Chat", icon=":material/chat:"),
    st.Page("views/archive.py", title="Trámites", icon=":material/book:", url_path="tramites"),
    st.Page("views/details.py", url_path="tramite", visibility="hidden"),
    st.Page("views/about.py", title="About Us", icon=":material/person:"),
]

# Navigation Bar
pg: Page = st.navigation(pages, position="top")
pg.run()
