import os
import requests
import streamlit as st

def get_api_base() -> str | None:
    return st.secrets.get("API_BASE") or os.getenv("API_BASE")

def _base() -> str:
    api_base = get_api_base()
    if not api_base:
        raise RuntimeError("API_BASE is not set. Please set it in Streamlit Secrets.")
    return api_base.rstrip("/")

def get(path: str, token: str | None = None, params: dict | None = None):
    url = f"{_base()}{path}"
    headers = {"accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return requests.get(url, headers=headers, params=params, timeout=30)

def post(path: str, token: str | None = None, json_body: dict | None = None, files=None, data=None):
    url = f"{_base()}{path}"
    headers = {"accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return requests.post(url, headers=headers, json=json_body, files=files, data=data, timeout=60)
