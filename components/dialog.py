import streamlit as st
from models.data_schema import IContent


@st.dialog(" ", width="large")
def data_detail_dialog(row: IContent) -> None:

    st.header(row.title, text_alignment="center")

    tab1, tab2, tab3 = st.tabs(["Descripción", "Indicaciones", "Observaciones"])

    with tab1.container(horizontal=False):
        tab1.write(row.description)

        tab1.subheader(":material/map: Ubicación")
        tab1.write(row.location)

        tab1.subheader(":material/browse: Sito Web")
        tab1.page_link(row.source, label="URL")

    with tab2.container(horizontal=False):
        if len(row.content) < 1:
            tab2.text("No disponible", width="stretch", text_alignment="center")
        else:
            for key, value in row.content.items():
                tab2.subheader(key)
                tab2.write(
                    "\n".join([f"{idx+1}. {val}" for idx, val in enumerate(value)])
                )

    with tab3.container(horizontal=False):
        if len(row.extra_content) < 1:
            tab3.text("No disponible", width="stretch", text_alignment="center")
        else:
            tab3.write(
                "\n".join(
                    [f"{idx+1}. {val}" for idx, val in enumerate(row.extra_content)]
                )
            )
