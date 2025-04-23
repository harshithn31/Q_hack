"""
FastAPI app entrypoint. Mounts API routes.
"""
from fastapi import FastAPI
from api.routes import router
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Personalized Learning Marketplace API")
app.include_router(router, prefix="/api")
