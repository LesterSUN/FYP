
import os
import requests
import streamlit as st

st.set_page_config(page_title="Settings", layout="wide")

def get_api_base() -> str | None:
    # 先读 secrets，再读环境变量
    return st.secrets.get("API_BASE") or os.getenv("API_BASE")

def norm_base(url: str) -> str:
    return url.rstrip("/")

st.title("Settings")

api_base = get_api_base()
st.write("API_BASE:", api_base if api_base else "❌ Not set")

st.divider()
st.subheader("Backend Health Check")

if not api_base:
    st.info('请到 Manage app → Secrets 里设置：\n\nAPI_BASE = "https://xxx.onrender.com"')
else:
    if st.button("Test GET /Health", type="primary"):
        try:
            url = f"{norm_base(api_base)}/Health"
            r = requests.get(url, timeout=30)
            st.write("Request URL:", url)
            st.write("HTTP Status:", r.status_code)

            # 尝试 JSON，否则显示文本
            try:
                st.json(r.json())
            except Exception:
                st.text(r.text)

            if r.status_code == 200:
                st.success("✅ FastAPI 后端可访问")
            else:
                st.warning("⚠️ 已连上，但接口返回非 200，请检查后端日志/路由")
        except Exception as e:
            st.error(f"❌ 请求失败：{e}")
