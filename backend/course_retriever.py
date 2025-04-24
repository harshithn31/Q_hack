"""
CourseRetriever: FAISS-backed semantic course retrieval using LangChain embeddings.
- Loads a mock course catalog (for MVP).
- Builds FAISS index on course descriptions.
- Retrieves top-N courses relevant to skills_gap.
"""
from typing import List, Dict
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
import os

import json

# Load real course catalog with modules from embeddings/courses.json
COURSE_JSON_PATH = os.path.join(os.path.dirname(__file__), "embeddings", "courses.json")
with open(COURSE_JSON_PATH, "r", encoding="utf-8") as f:
    ALL_COURSES = json.load(f)

class CourseRetriever:
    def __init__(self, courses: List[Dict] = None):
        self.courses = courses or ALL_COURSES
        self.embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
        self._build_index()

    def _build_index(self):
        # Reason: Build FAISS index on course descriptions (but keep full metadata)
        docs = [Document(page_content=course["description"], metadata=course) for course in self.courses]
        self.vectorstore = FAISS.from_documents(docs, self.embeddings)

    def retrieve(self, skills_gap: List[str], top_k: int = 3) -> List[Dict]:
        # Reason: Retrieve top-K courses relevant to skills_gap, returning full course dict (with modules)
        query = ", ".join(skills_gap)
        docs = self.vectorstore.similarity_search(query, k=top_k)
        # Return the original course dicts (with modules) for downstream LLM selection
        return [doc.metadata for doc in docs]
