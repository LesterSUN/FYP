import streamlit as st
from utils.state import init_state, logout
from utils.auth import login

init_state()
st.title("Login")

username = st.text_input("Username / Email", value=st.session_state.username or "")
password = st.text_input("Password", type="password")

col1, col2 = st.columns(2)

with col1:
    if st.button("Login", type="primary"):
        try:
            r = login(username, password)
            st.write("HTTP Status:", r.status_code)
            data = r.json()
            st.json(data)

            if r.status_code == 200 and "access_token" in data:
                st.session_state.token = data["access_token"]
                st.session_state.role = data.get("role")
                st.session_state.username = username
                st.success("✅ Login successful.")
            else:
                st.error("❌ Login failed.")
        except Exception as e:
            st.error(f"❌ Login request failed: {e}")

with col2:
    if st.button("Logout (clear session)"):
        logout()
        st.success("Session cleared.")
        st.rerun()

