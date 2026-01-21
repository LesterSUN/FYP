
import streamlit as st

def init_state():
    st.session_state.setdefault("token", None)
    st.session_state.setdefault("role", None)
    st.session_state.setdefault("username", None)

def logout():
    st.session_state.token = None
    st.session_state.role = None
    st.session_state.username = None
