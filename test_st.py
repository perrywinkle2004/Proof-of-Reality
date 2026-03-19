import streamlit as st

st.set_page_config(layout="wide")

try:
    st.set_page_config(layout="wide")
    print("SUCCESS: multiple calls allowed")
except Exception as e:
    print("ERROR:", e)
