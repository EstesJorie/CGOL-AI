from fastapi import FastAPI
from pydantic import BaseModel
import os
import sys
sys.path.insert(0, os.path.abspath("./build"))
import GameOfLife


app = FastAPI()

class Request(BaseModel):
    word: str

class Response(BaseModel):
    generations: int
    score: int

@app.post("/cgol", response_model=Response)
async def cgol(request: Request):
    generations, score = GameOfLife.game_of_life(request.word)
    return Response(generations=generations, score=score)
