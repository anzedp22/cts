from fastapi import FastAPI
from fastapi.responses import Response

CTS = FastAPI()


# Function to read version from version.txt
def read_version():
    with open("version.txt", "r") as file:
        version = file.read().strip()
    return version


# Hello path
@CTS.get("/")
def read_root():
    return {"msg": "Hello World"}


# Ping path
@CTS.get("/ping")
def ping():
    return Response(content=None, status_code=200)


# Version path
@CTS.get("/version")
def get_version():
    version = read_version()
    return {"version": version}
