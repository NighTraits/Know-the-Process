import streamlit as st

from pydantic import TypeAdapter

from models import KEY, IContent


def no_data_message():
    st.info("Trámite no encontrado.")
    with st.container(horizontal_alignment="center"):
        st.button("Regresar", on_click=prev_page)

def prev_page():
    st.switch_page("views/archive.py")

def page(data: IContent):
    with st.container(horizontal=False, width="content", border=True, horizontal_alignment="center"):
        st.title(data.title, text_alignment="center")
        st.write(data.description)
        with st.container(horizontal=True):
            with st.container(horizontal=False):
                st.subheader(":material/map: Ubicación")
                st.write(data.location)

            with st.container(horizontal=False):
                st.subheader(":material/browse: Sito Web")
                st.page_link(data.source, label="URL")

        with st.container(horizontal=False):
            st.subheader("Indicaciones")
            if len(data.content) < 1:
                st.text("No disponible")
            else:
                for key, value in data.content.items():
                    st.subheader(key)
                    st.write(
                        "\n".join([f"{idx+1}. {val}" for idx, val in enumerate(value)])
                    )

        with st.container(horizontal=False):
            st.subheader("Observaciones")
            if len(data.extra_content) < 1:
                st.text("No disponible")
            else:
                st.write(
                    "\n".join(
                        [f"{idx+1}. {val}" for idx, val in enumerate(data.extra_content)]
                    )
                )


if __name__=="__main__":
    
    msg_id = st.query_params.get("id")
    
    if not msg_id:
        no_data_message()
        st.stop()

    data = TypeAdapter(list[IContent]).validate_python(st.session_state[KEY.DATA])

    row = list(filter(lambda x: x.id == msg_id, data))

    if len(row) < 1:
        no_data_message()
        st.stop()

    page(row[0])

