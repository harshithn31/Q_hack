import os
import fitz  # PyMuPDF
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

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

    for q in questions:
        print(f"\n❓ Question: {q}")
        answer = query_resume(rag_chain, q)
        print(f"✅ Answer: {answer}")
