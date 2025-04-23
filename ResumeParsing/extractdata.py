import fitz  # PyMuPDF
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load API Key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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


def query_openai_resume_analysis(text: str, image_paths: list[str]) -> str:
    prompt = f"""
You are a smart resume reader. Given the extracted resume content below, extract and summarize:

- Work Experience
- Skills
- Projects
- Certifications
- Application Photo: If any image is detected, mention its filename.

Resume Text:
\"\"\"{text}\"\"\"

Resume Images:
{', '.join(image_paths) if image_paths else 'No image found.'}

Return the result in structured Markdown format.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts structured info from resumes."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    pdf_file = "SampleResumeHack.pdf"  # Replace with your file
    extracted = extract_text_and_images(pdf_file)

    print("📝 Extracting data using OpenAI...")
    result = query_openai_resume_analysis(extracted["text"], extracted["images"])
    print("\n🔍 Extraction Result:\n")
    print(result)