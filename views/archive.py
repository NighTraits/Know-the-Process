import streamlit as st

import pandas as pd
from uuid import uuid4
from pydantic import TypeAdapter

from models import IContent
from components import pop_up_message, data_detail_dialog


st.set_page_config(
    page_title="Archive",
    page_icon=":material/book:",
)

st.header("Archive")

if not st.session_state.data:
    st.info("No data found.")
    
else:
    if "df_key" not in st.session_state:
        st.session_state["df_key"] = str(uuid4())
        
    # Archive table    
    event = st.dataframe(
        pd.DataFrame(st.session_state.data)[["title", "location", "source", "updated_at"]],
        key=st.session_state["df_key"],
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
        width="stretch",
    )

    if len(rows := event.selection.rows) > 0:
        idx = rows[0]
        if idx > len(st.session_state.data):
            pop_up_message("Error", "Dato no encontrado")
        else:
            data = TypeAdapter(IContent).validate_python(st.session_state.data[idx])
            data_detail_dialog(data)
            