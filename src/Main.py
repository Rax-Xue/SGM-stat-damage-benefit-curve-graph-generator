import streamlit as st
from streamlit.logger import get_logger


LOGGER = get_logger(__name__)

def main_page():
    st.set_page_config(
        page_title="Start",
        page_icon="",  #FIXME:replace
    )

    st.sidebar.success("Select a page above.")

    f = open("README.md")
    content = f.read()
    st.markdown(content)

if __name__ == '__main__':
    main_page()


