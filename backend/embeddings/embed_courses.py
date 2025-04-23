"""
Embeds all course descriptions using OpenAI text-embedding-ada-002 and stores them in a FAISS index.
Saves metadata mapping for retrieval.
"""
import json
import os
from pathlib import Path
import faiss
import numpy as np
import openai
from dotenv import load_dotenv

COURSE_PATH = Path(__file__).parent / "courses.json"
INDEX_DIR = Path(__file__).parent / "faiss_index"
INDEX_DIR.mkdir(exist_ok=True)
INDEX_PATH = INDEX_DIR / "courses.index"
META_PATH = INDEX_DIR / "metadata.json"

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

EMBEDDING_MODEL = "text-embedding-ada-002"
EMBEDDING_DIM = 1536

with open(COURSE_PATH, "r", encoding="utf-8") as f:
    courses = json.load(f)

vectors = []
metadata = []

for course in courses:
    text = f"{course['title']}: {course['description']}"
    try:
        resp = openai.Embedding.create(input=text, model=EMBEDDING_MODEL)
        emb = resp["data"][0]["embedding"]
        vectors.append(emb)
        metadata.append(course)
        print(f"Embedded: {course['title']}")
    except Exception as e:
        print(f"Error embedding {course['title']}: {e}")

if not vectors:
    raise RuntimeError("No embeddings generated. Check OpenAI API key and input data.")

vectors_np = np.array(vectors).astype("float32")
index = faiss.IndexFlatL2(EMBEDDING_DIM)
index.add(vectors_np)
faiss.write_index(index, str(INDEX_PATH))
with open(META_PATH, "w", encoding="utf-8") as f:
    json.dump(metadata, f, ensure_ascii=False, indent=2)
print(f"Saved {len(vectors)} course embeddings to {INDEX_PATH} and metadata to {META_PATH}")
