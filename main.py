from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

class Req(BaseModel):
    message: str


@app.post("/data")
async def calculate(data:Req):
    print(data)
    return {"message":"post method"}


@app.get("/")
async def hello():
    return {"message":"hello world"}

