
import streamlit as st

def init_state():
    if "token" not in st.session_state:
        st.session_state.token = None
    if "role" not in st.session_state:
        st.session_state.role = None
    if "username" not in st.session_state:
        st.session_state.username = None

def logout():
    st.session_state.token = None
    st.session_state.role = None
    st.session_state.username = None
