import streamlit as st
import pandas as pd
from components import data_detail_dialog
from models import IContent
from pydantic import TypeAdapter

st.set_page_config(
    page_title="Archive",
    page_icon=":material/book:",
)

st.header("Archive")

event = st.dataframe(
    pd.DataFrame(st.session_state.data)[["title", "location", "source", "updated_at"]],
    key="table-tramites",
    column_config={
        "title": st.column_config.TextColumn(label="Trámite"),
        "location": st.column_config.TextColumn(label="Ubicación"),
        "source": st.column_config.LinkColumn(
            label="Sitio", width="small", display_text="link"
        ),
        "updated_at": st.column_config.DateColumn(
            label="Modificado",
        ),
    },
    column_order=("title", "location", "updated_at", "source"),
    hide_index=True,
    on_select="rerun",
    selection_mode="single-row",
    use_container_width=True,
)

if len(rows := event.selection.rows) > 0:
    data = TypeAdapter(IContent).validate_python(st.session_state.data[rows[0]])
    data_detail_dialog(data)
