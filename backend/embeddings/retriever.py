"""
Dummy retriever for course embeddings.
Replace with real FAISS vector search logic later.
"""
import json
from pathlib import Path
import random

COURSE_PATH = Path(__file__).parent / "courses.json"

with open(COURSE_PATH, "r", encoding="utf-8") as f:
    COURSES = json.load(f)

def retrieve_courses(skill_gap=None, top_n=3):
    """Return top_n random courses that match any skill in skill_gap."""
    if not skill_gap:
        return random.sample(COURSES, min(top_n, len(COURSES)))
    filtered = [c for c in COURSES if any(s.lower() in [sk.lower() for sk in c["skills"]] for s in skill_gap)]
    if len(filtered) < top_n:
        filtered += random.sample(COURSES, min(top_n - len(filtered), len(COURSES)))
    return filtered[:top_n]

# Usage: retrieve_courses(["Python", "React"])
