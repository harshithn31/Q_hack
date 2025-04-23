import os
import asyncio
#import uuid
import json
from dotenv import load_dotenv
from embeddings.utils import extract_resume_text, extract_images_from_pdf
from llm_agents.resume_agent import extract_with_agent
from typing import BinaryIO

# Load environment variables
load_dotenv()

# ----------- Resume Processing Pipeline -----------
async def process_resume(file: BinaryIO, filename: str):
    try:
        resume_text = extract_resume_text(file, filename)
        print("\n✅ Resume text extracted.")

        avatar_uri = None
        if filename.lower().endswith(".pdf"):
            image_paths = extract_images_from_pdf(file)
            print("🖼️ Images extracted:", image_paths)
            avatar_uri = image_paths[0] if image_paths else None

        print("\n🤖 Extracting structured data with ResumeAgent...")
        result = await extract_with_agent(resume_text)  # 👈 Corrected here

        name = next((line.strip() for line in resume_text.splitlines() if line.strip()), "Unknown")

        output = {
            "name": name,
            "avatarUri": avatar_uri,
            "summary": result.summary,
            "skills": result.skills
        }

        print("\n📦 JSON Output:")
        print(output)
        return output

    except Exception as e:
        print(f"\n❌ Error processing resume: {e}")
        return None


# ----------- Main Runner -----------
if __name__ == "__main__":
    filename = input("Enter the path to the resume file (.pdf or .txt): ").strip()

    if not os.path.isfile(filename):
        print(f"❌ File not found: {filename}")
    else:
        with open(filename, "rb") as f:
            file_bytes = f.read()
            process_resume(file_bytes, filename)
