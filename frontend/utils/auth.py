from .api import api_post

def login(username: str, password: str):
    payload = {"username": username, "password": password}
    return api_post("/auth/login", json_body=payload)


