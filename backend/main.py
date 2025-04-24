from fastapi import FastAPI
from api.routes import router
from dotenv import load_dotenv
import os
import resume_parser_main
import uvicorn

load_dotenv()

app = FastAPI(title="Personalized Learning Marketplace API")
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
