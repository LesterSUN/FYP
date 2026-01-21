import streamlit as st
from utils.state import init_state, logout
from utils.api import get_api_base

st.set_page_config(page_title="EMR Structuring System", layout="wide")
init_state()

st.title("EMR Structuring System (Prototype)")

with st.sidebar:
    st.header("Connection")
    api_base = get_api_base()
    st.write("API_BASE:", api_base if api_base else "❌ Not set")

    st.divider()
    st.header("Session")
    st.write("Logged in as:", st.session_state.username or "-")
    st.write("Role:", st.session_state.role or "-")

    if st.session_state.token:
        st.success("Logged in")
        if st.button("Logout"):
            logout()
            st.rerun()
    else:
        st.info("Not logged in")

st.markdown(
    """
### 使用说明
请从左侧页面导航进入：

- **Login**：登录获取 token（写入 session）
- **Doctor**：提交 EMR、查看 Records
- **Admin**：查看 Audit Logs（仅 Admin）
- **Settings**：健康检查 `/Health`、查看 API_BASE
"""
)

