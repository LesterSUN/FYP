import streamlit as st
from utils.state import init_state
from utils.api import api_get

init_state()
st.title("Admin")

if not st.session_state.token:
    st.warning("Please login first (go to Login page).")
    st.stop()

if st.session_state.role != "Admin":
    st.error("Admin role required.")
    st.stop()

st.subheader("Audit Logs")
if st.button("Load audit logs", type="primary"):
    try:
        r = api_get("/admin/logs", token=st.session_state.token)
        st.write("HTTP Status:", r.status_code)
        try:
            st.json(r.json())
        except Exception:
            st.text(r.text)
    except Exception as e:
        st.error(f"❌ Failed to load audit logs: {e}")

