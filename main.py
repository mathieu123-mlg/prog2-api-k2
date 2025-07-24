from fastapi import FastAPI, requests
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse

app = FastAPI()


@app.get("/hello")
def read_hello(request: Request, name: str="Non fourni", is_teacher: bool=None):
    if (name == "Non fourni") and (is_teacher is None):
        accept_headers = request.headers.get("Accept")
        if accept_headers != "text/plain":
            return JSONResponse({"message": "Unsupported Media Type"}, status_code=400)
        return JSONResponse(content="Hello world", status_code=200)
    else:
        if is_teacher:
            result = f"Hello Teacher {name}!"
        else:
            result = f"Hello {name}!"
        return {"message": result}


class WelcomeRequest(BaseModel):
    name: str

@app.post("/welcome")
def welcome_user(request: WelcomeRequest):
    return {f"Bienvenue {request.name}"}


class SecretCodeRequest(BaseModel):
    secret_code: int

@app.put("/top-secret")
def put_top_secret(request: Request, request_body: SecretCodeRequest):
    auth_headers = request.headers.get("Authorization")

    if auth_headers != "my-secret-key":
        return JSONResponse(
            status_code=403,
            content={"error": f"Unauthorized header received: {auth_headers}"}
        )

    secret_code = request_body.secret_code
    code_length = len(str(secret_code))
    if code_length != 4:
        return JSONResponse(
            status_code=400,
            content={"error": f"Le code fourni n'est pas à 4 chiffre mais à {code_length} chiffres."}
        )
    return JSONResponse(content={"message": f"Voici le code {secret_code}"}, status_code=200)
