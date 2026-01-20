import streamlit as st
import os

st.title("EMR Structuring System (Prototype)")

api_base = st.secrets.get("API_BASE", None)  # Streamlit Cloud 推荐读法
st.write("API_BASE from secrets:", api_base)

# 也顺便看一下环境变量（有些人用 env var 的方式）
st.write("API_BASE from env:", os.getenv("API_BASE"))

st.info("If API_BASE is None, your Secrets may not be saved or not propagated yet.")

