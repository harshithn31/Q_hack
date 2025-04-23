import os
import fitz  # PyMuPDF
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

# ----------- Step 1: Extract text and images from PDF -----------
def extract_text_and_images(pdf_path: str, output_dir: str = "images") -> dict:
    doc = fitz.open(pdf_path)
    full_text = ""
    image_paths = []

    os.makedirs(output_dir, exist_ok=True)

    for i, page in enumerate(doc):
        full_text += page.get_text() + "\n"

        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_filename = f"{output_dir}/page{i+1}_img{img_index+1}.{image_ext}"

            with open(image_filename, "wb") as f:
                f.write(image_bytes)
            image_paths.append(image_filename)

    return {"text": full_text.strip(), "images": image_paths}


# ----------- Step 2: Apply RAG -----------
def build_rag_pipeline(resume_text: str) -> RetrievalQA:
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    resume_chunks = splitter.split_text(resume_text)

    print(f"\n🧩 Total Chunks: {len(resume_chunks)}")
    for i, chunk in enumerate(resume_chunks):
        print(f"\n--- Chunk {i + 1} ---\n{chunk}\n")

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(resume_chunks, embedding=embeddings)

    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model="gpt-4o-mini"),
        retriever=vectorstore.as_retriever(),
        return_source_documents=True
    )
    return qa_chain


# ----------- Step 3: Query the Resume -----------
def query_resume(qa_chain: RetrievalQA, query: str):
    result = qa_chain.invoke({"query": query})
    return result['result']


# ----------- Step 4: Agent Definition -----------
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
    pdf_file = "SampleResumeHack.pdf"  # Replace with your resume path

    # Extract content from resume
    extracted = extract_text_and_images(pdf_file)
    resume_text = extracted["text"]
    resume_images = extracted["images"]

    print("\n📄 Resume text extracted.")
    print("🖼️ Images found:", resume_images)

    # Build the RAG pipeline
    rag_chain = build_rag_pipeline(resume_text)

    # Ask questions
    questions = [
        "What work experience does this candidate have?",
        "List all technical skills.",
        "What projects are mentioned?",
        "Does the resume mention any certifications?",
        "Is there a photo attached in the application?"
    ]

    #for q in questions:
    #    print(f"\n❓ Question: {q}")
    #    answer = query_resume(rag_chain, q)
    #    print(f"✅ Answer: {answer}")

    # Use ResumeAgent for structured extraction
    print("\n🤖 Extracting structured data using ResumeAgent...")
    # Use RAG to get focused chunks
    retrieved_docs = rag_chain.retriever.invoke("Extract technical skills and summary from this resume.")
    combined_rag_text = "\n".join([doc.page_content for doc in retrieved_docs])

    # Optional: print what you're feeding the agent
    print("\n📥 Text passed to ResumeAgent:\n", combined_rag_text[:500])

    structured_result = asyncio.run(extract_with_agent(combined_rag_text))

    print("\n🧠 Agent Output:")
    print("Skills:", structured_result.skills)
    print("Summary:", structured_result.summary)
