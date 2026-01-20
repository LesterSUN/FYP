import streamlit as st
from utils.state import init_state
from utils.api import get

st.set_page_config(page_title="Admin", layout="wide")
init_state()

st.header("Admin Workspace")

if not st.session_state.token:
    st.warning("Please login first (go to Login page).")
    st.stop()

if st.session_state.role != "Admin":
    st.error("Admin role required.")
    st.stop()

st.subheader("Audit Logs")
filters = st.text_input("filters (optional)", value="")
if st.button("Load audit logs", type="primary"):
    params = {"filters": filters} if filters.strip() else None
    r = get("/admin/logs", token=st.session_state.token, params=params)
    st.write("HTTP:", r.status_code)
    try:
        st.json(r.json())
    except Exception:
        st.text(r.text)
