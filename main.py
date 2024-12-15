import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from typing import Annotated
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from endpoints.recommendation import findRecommendations, Item

app = FastAPI()

origins = methods = headers = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=headers
)


@app.get("/")
def root():
    return {
        "message": "API is up and running"
    }
    
@app.get("/recommendations")
def recommendations(data: Annotated[Item, Query()]):
    return findRecommendations(data)