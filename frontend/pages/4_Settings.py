
import streamlit as st
from utils.api import get_api_base, api_get

st.title("Settings")
st.subheader("Backend Health Check")

api_base = get_api_base()
st.write("API_BASE:", api_base if api_base else "❌ Not set")

if st.button("Test GET /Health", type="primary"):
    try:
        r = api_get("/Health")
        st.write("HTTP Status:", r.status_code)
        try:
            st.json(r.json())
        except Exception:
            st.text(r.text)

        if r.status_code == 200:
            st.success("✅ Connected to FastAPI successfully.")
        else:
            st.warning("⚠️ Connected, but endpoint returned non-200.")
    except Exception as e:
        st.error(f"❌ Request failed: {e}")
