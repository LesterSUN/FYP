import streamlit as st
from .api import post

def login(username: str, password: str):
    payload = {"username": username, "password": password}
    r = post("/auth/login", json_body=payload)
    data = r.json() if r.headers.get("content-type", "").startswith("application/json") else {"raw": r.text}

    if r.status_code == 200 and "access_token" in data:
        st.session_state.token = data.get("access_token")
        st.session_state.role = data.get("role")
        st.session_state.username = username
        return True, data

    return False, data

