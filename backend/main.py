from fastapi import FastAPI

from backend.database.connection import engine
from backend.database.base import Base

import backend.models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CustomerSphere AI"
)

@app.get("/")
def home():
    return {
        "message": "CustomerSphere AI Backend Running"
    }