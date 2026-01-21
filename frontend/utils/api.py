import os
import requests
import streamlit as st

def get_api_base() -> str | None:
    # 优先 secrets，其次环境变量
    return st.secrets.get("API_BASE") or os.getenv("API_BASE")

def norm_base(url: str) -> str:
    return url.rstrip("/")

def api_get(path: str, token: str | None = None, params: dict | None = None):
    base = get_api_base()
    if not base:
        raise RuntimeError("API_BASE is not set. Please set it in Streamlit Secrets.")
    url = f"{norm_base(base)}{path}"
    headers = {"accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return requests.get(url, headers=headers, params=params, timeout=30)

def api_post(path: str, token: str | None = None, json_body: dict | None = None, files=None, data=None):
    base = get_api_base()
    if not base:
        raise RuntimeError("API_BASE is not set. Please set it in Streamlit Secrets.")
    url = f"{norm_base(base)}{path}"
    headers = {"accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return requests.post(url, headers=headers, json=json_body, files=files, data=data, timeout=60)
