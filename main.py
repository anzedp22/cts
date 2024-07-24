from fastapi import FastAPI
from fastapi.responses import Response

CTS = FastAPI()


# Hello path
@CTS.get("/")
def read_root():
    return {"msg": "Hello World"}


# Ping path
@CTS.get("/ping")
def ping():
    return Response(content=None, status_code=200)
