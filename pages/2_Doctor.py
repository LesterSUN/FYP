import streamlit as st
from utils.state import init_state
from utils.api import post, get

st.set_page_config(page_title="Doctor", layout="wide")
init_state()

st.header("Doctor Workspace")

if not st.session_state.token:
    st.warning("Please login first (go to Login page).")
    st.stop()

if st.session_state.role not in ["Doctor", "Admin"]:
    st.error("You do not have permission to access Doctor functions.")
    st.stop()

tab1, tab2 = st.tabs(["Extract", "Records"])

with tab1:
    st.subheader("Submit EMR and Extract")
    model_version = st.text_input("model_version (optional)", value="v1")

    mode = st.radio("Input type", ["Paste text", "Upload file"], horizontal=True)

    if mode == "Paste text":
        text = st.text_area("De-identified EMR text", height=220)
        if st.button("Run Extract", type="primary"):
            if not text.strip():
                st.error("Text is empty.")
            else:
                r = post(
                    "/extract",
                    token=st.session_state.token,
                    json_body={"text": text, "model_version": model_version},
                )
                st.write("HTTP:", r.status_code)
                try:
                    st.json(r.json())
                except Exception:
                    st.text(r.text)

    else:
        up = st.file_uploader("Upload .txt", type=["txt"])
        if st.button("Run Extract (file)", type="primary"):
            if not up:
                st.error("No file uploaded.")
            else:
                files = {"file": (up.name, up.getvalue(), "text/plain")}
                data = {"model_version": model_version}
                r = post("/extract", token=st.session_state.token, files=files, data=data)
                st.write("HTTP:", r.status_code)
                try:
                    st.json(r.json())
                except Exception:
                    st.text(r.text)

with tab2:
    st.subheader("Records List / Detail")

    col1, col2, col3 = st.columns(3)
    with col1:
        page = st.number_input("page", min_value=1, value=1, step=1)
    with col2:
        page_size = st.number_input("page_size", min_value=1, max_value=100, value=10, step=1)
    with col3:
        if st.button("Load records", type="primary"):
            r = get("/records", token=st.session_state.token, params={"page": int(page), "page_size": int(page_size)})
            st.write("HTTP:", r.status_code)
            try:
                st.json(r.json())
            except Exception:
                st.text(r.text)

    st.divider()
    rid = st.text_input("Record id")
    if st.button("View record detail (/records/{id})"):
        if not rid.strip():
            st.error("Please input record id.")
        else:
            r = get(f"/records/{rid}", token=st.session_state.token)
            st.write("HTTP:", r.status_code)
            try:
                st.json(r.json())
            except Exception:
                st.text(r.text)
