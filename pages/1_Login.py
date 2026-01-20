import streamlit as st
from utils.state import init_state, logout
from utils.auth import login

st.set_page_config(page_title="Login", layout="wide")
init_state()

st.header("Login")

username = st.text_input("Username / Email", value=st.session_state.username or "")
password = st.text_input("Password", type="password")

col1, col2 = st.columns(2)

with col1:
    if st.button("Login", type="primary"):
        ok, data = login(username, password)
        st.write("Response:")
        st.json(data)
        if ok:
            st.success("✅ Login success")
            st.rerun()
        else:
            st.error("❌ Login failed")

with col2:
    if st.button("Clear session (Logout)"):
        logout()
        st.success("Cleared.")
        st.rerun()
