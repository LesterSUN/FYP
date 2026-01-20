from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="FYP Backend API")

class LoginRequest(BaseModel):
    username: str
    password: str

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/auth/login")
def login(req: LoginRequest):
    # demo: always succeed; later replace with real auth/RBAC
    role = "Admin" if req.username.lower().startswith("admin") else "Doctor"
    return {"access_token": "demo-token", "role": role}
