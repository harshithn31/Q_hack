import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from pydantic import BaseModel, Field
from pydantic_ai import Agent
import asyncio

# Load API Key from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ----------- Step 1: Apply Chunking -----------
def chunk_resume_text(resume_text: str):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    resume_chunks = splitter.split_text(resume_text)

    print(f"\n🧩 Total Chunks: {len(resume_chunks)}")
    for i, chunk in enumerate(resume_chunks):
        print(f"\n--- Chunk {i + 1} ---\n{chunk}\n")

    return resume_chunks


# ----------- Step 2: Build RAG Retrieval Pipeline -----------
def build_rag_retriever(resume_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(resume_chunks, embedding=embeddings)
    retriever = vectorstore.as_retriever()
    return retriever


# ----------- Step 3: Agent Definition -----------
class ResumeAgentOutput(BaseModel):
    skills: list[str] = Field(..., description="List of extracted skills.")
    summary: str = Field(..., description="Short summary of the candidate.")

resume_agent = Agent(
    "openai:gpt-4o-mini",
    api_key=OPENAI_API_KEY,
    output_type=ResumeAgentOutput,
    system_prompt=(
        "You are an expert career assistant. Based ONLY on the provided resume text, "
        "extract a JSON array of the candidate's key technical skills (use exact terms found in the text, no guessing, lowercase, no duplicates), "
        "and write a 1–2 sentence summary of the candidate's experience based strictly on what’s written. "
        "Do not create information not present in the text. Respond in this JSON format: {\"skills\": [...], \"summary\": \"...\"}"
    ),
)

async def extract_with_agent(text):
    result = await resume_agent.run(text)
    return result.output


# ----------- Main Runner -----------
if __name__ == "__main__":
    # Simulate input from utils.py
    from utils import extract_text_and_images

    pdf_file = "SampleResumeHack.pdf"
    extracted = extract_text_and_images(pdf_file)
    resume_text = extracted["text"]

    # Step 1: Chunk the resume text
    resume_chunks = chunk_resume_text(resume_text)

    # Step 2: Build retriever from chunks
    retriever = build_rag_retriever(resume_chunks)

    # Step 3: Use retriever to get relevant chunks
    print("\n🔍 Retrieving relevant chunks for summarization...")
    retrieved_docs = retriever.invoke("Extract technical skills and summary from this resume.")
    combined_rag_text = "\n".join([doc.page_content for doc in retrieved_docs])

    print("\n📥 Text passed to ResumeAgent:\n", combined_rag_text[:500])

    # Step 4: Use ResumeAgent
    print("\n🤖 Extracting structured data using ResumeAgent...")
    structured_result = asyncio.run(extract_with_agent(combined_rag_text))

    print("\n🧠 Agent Output:")
    print("Skills:", structured_result.skills)
    print("Summary:", structured_result.summary)
