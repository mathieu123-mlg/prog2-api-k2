from fastapi import FastAPI
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from typing import List

app = FastAPI()


# Q1: GET /ping sans parametre
@app.get("/ping")
def read_ping():
    return {f"pong"}


# Q2: GET /home sans parametre
@app.get("/home")
def welcome_home():
    with open("welcome.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return Response(content=html_content, status_code=200, content_type="text/html", media_type="text/html")


# Q3: GET /{full_path:path}
@app.get("/{full_path:path}")
def read_path(full_path: str):
    with open("error_welcome.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return Response(content=html_content, status_code=404, media_type="text/html")


# Q4: POST /posts
class PostModel(BaseModel):
    author: str
    title: str
    content: str
    creation_datetime: str

post_store: List[PostModel] = []

def serialized_stored_player():
    return [player.model_dump() for player in post_store]

@app.post("/posts")
def post_posts(post_lists: List[PostModel]):
    post_store.extend(post_lists)
    return JSONResponse(
        content={ "players": serialized_stored_player() },
        status_code=201
    )


# Q5: PUT /posts
@app.put("/posts")
def put_posts(post_lists: List[PostModel]):
    found = False
    for player in post_lists:
        found = False
        for i, existing_post in enumerate(post_store):
            if existing_post.name == player.name:
                post_store[i] = player
                found = True
                break
    if not found:
        post_store.append(player)