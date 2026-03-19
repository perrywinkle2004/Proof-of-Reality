import streamlit as st

st.set_page_config(layout="wide")

original_markdown = st.markdown
def custom_markdown(body, unsafe_allow_html=False, **kwargs):
    if unsafe_allow_html and isinstance(body, str):
        body = '\n'.join(line.lstrip() for line in body.split('\n'))
    return original_markdown(body, unsafe_allow_html=unsafe_allow_html, **kwargs)
st.markdown = custom_markdown

st.markdown("""
    <!-- SHOULD NO LONGER BE CODE BLOCK -->
    <div style="color: red;">
        HELLO RED
    </div>
""", unsafe_allow_html=True)
