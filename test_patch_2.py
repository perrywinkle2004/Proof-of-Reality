import streamlit as st
import textwrap

import app

col = st.columns(1)[0]
col.markdown('    <div>1</div>', unsafe_allow_html=True)
st.sidebar.markdown('    <div>2</div>', unsafe_allow_html=True)
st.markdown('    <div>3</div>', unsafe_allow_html=True)
print("No crashes!")
