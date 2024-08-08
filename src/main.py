import uvicorn
from fastapi import FastAPI
from os import getenv

from src.routers import molecules

app = FastAPI(title="Python Summer School 2024: SMILES")
app.include_router(molecules.router)


@app.get("/")
def get_server():
    return {"server_id": getenv("SERVER_ID", "1")}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
