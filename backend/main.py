"""
FastAPI app entrypoint. Mounts API routes.
"""
import os
os.environ["OPENAI_API_KEY"] = "sk-proj-UPJGUS4d-tqa2abENjdFxM55wbdplQmZcvIwAM66vXClxx1jlQz9-6eG2KSKJ_KSiE9gOj2BHT3BlbkFJygRzc_TVc32uZEajL3WQJslCECbH9PqEwjhjZkKpCPlP4GuL9mp7M16y-2vqTzm_IpatoSKLIA"

from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="Personalized Learning Marketplace API")
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
