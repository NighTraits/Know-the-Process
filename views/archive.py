import streamlit as st

from pydantic import TypeAdapter
from dataclasses import replace

from models import KEY, IContent


@st.cache_data
def generate_link_column(data: list[IContent])-> list[IContent]:
    return [replace(dt, id=f"/tramite?id={dt.id}") for dt in data]


def clear_filter() -> None:
    st.session_state["input-search"] = ""
    st.session_state["select-search"] = ""
    
    
def set_filters(data: list[IContent]) -> list[IContent]:
    filter_data_1 = list(set([dt.location for dt in data]))
    with st.container(horizontal=True, vertical_alignment="bottom"):
        if (search:=st.text_input("Búsqueda por trámite", key="input-search", placeholder="Escribe aquí...")):
            data = list(filter(lambda x: (search).lower() in x.title.lower(), data))
        
        if (selected:=st.selectbox("Institución", filter_data_1, key="select-search", index=None, accept_new_options=True, placeholder="Elige una opción")):
            data = list(filter(lambda x: x.location == selected, data))
        
        st.button("Limpiar filtro", on_click=clear_filter)
    
    return data


def set_pagination(data: list[IContent]) -> tuple[int, int]:
    with st.container(horizontal_alignment="right"):
        rows_per_page = 15    
        total_pages = (len(data) + rows_per_page - 1) // rows_per_page
        page = st.pagination(num_pages=total_pages)
        
    start_idx = (page - 1) * rows_per_page
    end_idx = start_idx + rows_per_page
    return start_idx, end_idx

# Page Main Body
def page(data_raw: list[IContent]) -> None:
    # replace with redirect link
    data = generate_link_column(data_raw)

    # filters
    data = set_filters(data)

    if not data:
        st.info("No coincidencias")
        st.stop()

    # dataframe table init (to be shown on top of the pagination)
    table = st.empty()
    
    # pagination init
    start_idx, end_idx = set_pagination(data)
    
    # dataframe table setup
    table.dataframe(
        data[start_idx:end_idx],
        column_config={
            "id": st.column_config.LinkColumn(
                "",
                display_text="Detalles",
                width="small",
            ),
            "title": st.column_config.TextColumn(label="Trámite"),
            "location": st.column_config.TextColumn(label="Ubicación"),
            "source": st.column_config.LinkColumn(
                label="URL", width="small", display_text="link",
            ),
        },
        column_order=("id","title", "location", "source"),
        hide_index=True,
        width="stretch",
        height="content"
    )

if __name__=="__main__":
    
    st.set_page_config(page_title="Archive", page_icon=":material/book:")
    st.title("Trámites")
    
    if not (data_raw:=TypeAdapter(list[IContent]).validate_python(st.session_state[KEY.DATA])):
        st.error("No se encontraron trámites disponibles.")
        st.stop()
        
    page(data_raw)
