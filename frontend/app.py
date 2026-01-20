import os
import json
import requests
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="EMR Structuring System", layout="wide")
st.title("EMR Structuring System (Prototype)")

# -------------------------
# Helpers
# -------------------------
def get_api_base() -> str | None:
    # Prefer Streamlit secrets, fallback to env
    return st.secrets.get("API_BASE") or os.getenv("API_BASE")

def norm_base(url: str) -> str:
    return url.rstrip("/")

def api_get(path: str, token: str | None = None, params: dict | None = None):
    api_base = get_api_base()
    if not api_base:
        raise RuntimeError("API_BASE is not set in Streamlit Secrets or environment variables.")
    url = f"{norm_base(api_base)}{path}"
    headers = {"accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    r = requests.get(url, headers=headers, params=params, timeout=30)
    return r

def api_post(path: str, token: str | None = None, json_body: dict | None = None, files=None, data=None):
    api_base = get_api_base()
    if not api_base:
        raise RuntimeError("API_BASE is not set in Streamlit Secrets or environment variables.")
    url = f"{norm_base(api_base)}{path}"
    headers = {"accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    # If files are used, don't set Content-Type manually (requests will set it)
    r = requests.post(url, headers=headers, json=json_body, files=files, data=data, timeout=60)
    return r

def pretty_json(obj):
    st.code(json.dumps(obj, ensure_ascii=False, indent=2), language="json")

# -------------------------
# Sidebar: API + Session
# -------------------------
with st.sidebar:
    st.header("Connection")
    api_base = get_api_base()
    st.write("API_BASE:", api_base if api_base else "❌ Not set")

    if "token" not in st.session_state:
        st.session_state.token = None
    if "role" not in st.session_state:
        st.session_state.role = None
    if "username" not in st.session_state:
        st.session_state.username = None

    st.divider()
    st.header("Session")
    st.write("Logged in as:", st.session_state.username or "-")
    st.write("Role:", st.session_state.role or "-")
    if st.session_state.token:
        st.success("Token stored in session")
    else:
        st.info("Not logged in")

# -------------------------
# Main Tabs
# -------------------------
tabs = st.tabs(["1) Health Check", "2) Login", "3) Doctor: Extract", "4) Doctor: Records", "5) Admin: Audit Logs"])

# 1) Health Check
with tabs[0]:
    st.subheader("Backend Health Check")
    st.write("Use this to verify Streamlit can reach your FastAPI service on Render.")

    col1, col2 = st.columns([1, 2])
    with col1:
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

    with col2:
        st.caption("If you see an error, check: API_BASE, Render service status, CORS, and endpoint path capitalization.")
        st.caption("You showed your docs has `/Health` (capital H). So we call `/Health` here.")

# 2) Login
with tabs[1]:
    st.subheader("Login")
    st.write("This calls POST `/auth/login` to obtain an access token and role.")

    username = st.text_input("Username / Email", value=st.session_state.username or "")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("Login", type="primary"):
            try:
                payload = {"username": username, "password": password}
                r = api_post("/auth/login", json_body=payload)
                st.write("HTTP Status:", r.status_code)
                data = r.json() if r.headers.get("content-type", "").startswith("application/json") else {"raw": r.text}
                pretty_json(data)

                if r.status_code == 200 and "access_token" in data:
                    st.session_state.token = data.get("access_token")
                    st.session_state.role = data.get("role")
                    st.session_state.username = username
                    st.success("✅ Login successful. Token saved in session.")
                else:
                    st.error("❌ Login failed. Check credentials or backend implementation.")
            except Exception as e:
                st.error(f"❌ Login request failed: {e}")

    with col2:
        if st.button("Logout (clear session)"):
            st.session_state.token = None
            st.session_state.role = None
            st.session_state.username = None
            st.success("Session cleared.")

# 3) Doctor: Extract
with tabs[2]:
    st.subheader("Doctor: Submit EMR Text / File and Extract")
    st.write("This calls POST `/extract`. Requires Doctor role in your design.")

    if not st.session_state.token:
        st.warning("Please login first.")
    else:
        # Basic role gate (frontend display only; backend RBAC should still enforce)
        if st.session_state.role not in ["Doctor", "Admin"]:
            st.error("Your current role cannot access this feature.")
        else:
            model_version = st.text_input("Model version (optional)", value="v1")

            mode = st.radio("Input type", ["Paste text", "Upload file"], horizontal=True)

            if mode == "Paste text":
                text = st.text_area("De-identified EMR text", height=200, placeholder="Paste EMR text here...")
                if st.button("Run Extract", type="primary"):
                    if not text.strip():
                        st.error("Text is empty.")
                    else:
                        try:
                            payload = {"text": text, "model_version": model_version}
                            r = api_post("/extract", token=st.session_state.token, json_body=payload)
                            st.write("HTTP Status:", r.status_code)
                            try:
                                data = r.json()
                                st.json(data)
                            except Exception:
                                st.text(r.text)
                        except Exception as e:
                            st.error(f"❌ Extract failed: {e}")

            else:
                uploaded = st.file_uploader("Upload .txt file (de-identified)", type=["txt"])
                if st.button("Run Extract (file)", type="primary"):
                    if not uploaded:
                        st.error("No file uploaded.")
                    else:
                        try:
                            # If your backend expects multipart with 'file', adjust key if different
                            files = {"file": (uploaded.name, uploaded.getvalue(), "text/plain")}
                            # Some backends also accept model_version via form field
                            data = {"model_version": model_version}
                            r = api_post("/extract", token=st.session_state.token, files=files, data=data)
                            st.write("HTTP Status:", r.status_code)
                            try:
                                st.json(r.json())
                            except Exception:
                                st.text(r.text)
                        except Exception as e:
                            st.error(f"❌ Extract failed: {e}")

# 4) Doctor: Records
with tabs[3]:
    st.subheader("Doctor: View Records")
    st.write("This calls GET `/records` and GET `/records/{id}` and GET `/records/{id}/download` (for demo).")

    if not st.session_state.token:
        st.warning("Please login first.")
    else:
        if st.session_state.role not in ["Doctor", "Admin"]:
            st.error("Your current role cannot access records.")
        else:
            col1, col2, col3 = st.columns(3)
            with col1:
                page = st.number_input("page", min_value=1, value=1, step=1)
            with col2:
                page_size = st.number_input("page_size", min_value=1, max_value=100, value=10, step=1)
            with col3:
                if st.button("Load records", type="primary"):
                    try:
                        r = api_get("/records", token=st.session_state.token, params={"page": int(page), "page_size": int(page_size)})
                        st.write("HTTP Status:", r.status_code)
                        data = r.json() if r.headers.get("content-type", "").startswith("application/json") else {"raw": r.text}
                        pretty_json(data)
                    except Exception as e:
                        st.error(f"❌ Failed to load records: {e}")

            st.divider()
            record_id = st.text_input("Record id to view/download (e.g., from /records list)", value="")
            colA, colB = st.columns(2)
            with colA:
                if st.button("GET /records/{id}"):
                    if not record_id.strip():
                        st.error("Please enter record id.")
                    else:
                        try:
                            r = api_get(f"/records/{record_id}", token=st.session_state.token)
                            st.write("HTTP Status:", r.status_code)
                            try:
                                st.json(r.json())
                            except Exception:
                                st.text(r.text)
                        except Exception as e:
                            st.error(f"❌ Failed: {e}")
            with colB:
                fmt = st.selectbox("download format", ["json", "csv"])
                if st.button("Download (calls endpoint)"):
                    if not record_id.strip():
                        st.error("Please enter record id.")
                    else:
                        try:
                            r = api_get(f"/records/{record_id}/download", token=st.session_state.token, params={"format": fmt})
                            st.write("HTTP Status:", r.status_code)
                            # In many backends this returns a file; here we just show text for demo
                            st.text(r.text[:2000])
                            st.info("If backend returns a real file attachment, you can handle it with st.download_button.")
                        except Exception as e:
                            st.error(f"❌ Failed: {e}")

# 5) Admin: Audit Logs
with tabs[4]:
    st.subheader("Admin: View Audit Logs")
    st.write("This calls GET `/admin/logs`. Admin role only.")

    if not st.session_state.token:
        st.warning("Please login first.")
    else:
        if st.session_state.role != "Admin":
            st.error("Admin role required.")
        else:
            filters = st.text_input("Filters (optional, e.g., user=xxx or date range)", value="")
            if st.button("Load audit logs", type="primary"):
                try:
                    params = {"filters": filters} if filters.strip() else None
                    r = api_get("/admin/logs", token=st.session_state.token, params=params)
                    st.write("HTTP Status:", r.status_code)
                    try:
                        st.json(r.json())
                    except Exception:
                        st.text(r.text)
                except Exception as e:
                    st.error(f"❌ Failed to load audit logs: {e}")

st.caption(f"Last loaded: {datetime.utcnow().isoformat()}Z")
