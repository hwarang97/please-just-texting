from app.routers import conversations
from app.routers import default
from app.routers import users
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.testclient import TestClient

app = FastAPI()
app.include_router(default.router)
app.include_router(users.router)
app.include_router(conversations.router)
templates = Jinja2Templates(directory="app/templates")

client = TestClient(app)


def test_read_default() -> None:
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/docs"
