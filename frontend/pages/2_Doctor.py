import streamlit as st
from utils.state import init_state
from utils.api import api_get, api_post

init_state()
st.title("Doctor")

if not st.session_state.token:
    st.warning("Please login first (go to Login page).")
    st.stop()

if st.session_state.role not in ["Doctor", "Admin"]:
    st.error("Your role cannot access Doctor functions.")
    st.stop()

tab1, tab2 = st.tabs(["Extract", "Records"])

with tab1:
    st.subheader("Submit EMR Text and Extract")
    text = st.text_area("De-identified EMR text", height=200)
    if st.button("Run Extract", type="primary"):
        if not text.strip():
            st.error("Text is empty.")
        else:
            try:
                r = api_post("/extract", token=st.session_state.token, json_body={"text": text})
                st.write("HTTP Status:", r.status_code)
                try:
                    st.json(r.json())
                except Exception:
                    st.text(r.text)
            except Exception as e:
                st.error(f"❌ Extract failed: {e}")

with tab2:
    st.subheader("View Records")
    if st.button("Load records", type="primary"):
        try:
            r = api_get("/records", token=st.session_state.token)
            st.write("HTTP Status:", r.status_code)
            try:
                st.json(r.json())
            except Exception:
                st.text(r.text)
        except Exception as e:
            st.error(f"❌ Failed to load records: {e}")

