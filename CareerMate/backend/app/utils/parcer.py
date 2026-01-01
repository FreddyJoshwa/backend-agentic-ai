from PyPDF2 import PdfReader
import docx2txt
import os
from openai import OpenAI
import os

# Initialize OpenAI client
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

def parse_resume(file_path: str) -> str:
    """
    Takes a file path (PDF or DOCX) and returns extracted text.
    """
    ext = os.path.splitext(file_path)[1].lower()
    text = ""

    if ext == ".pdf":
        try:
            reader = PdfReader(file_path)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        except Exception as e:
            print("Error reading PDF:", e)
    elif ext in [".docx", ".doc"]:
        try:
            text = docx2txt.process(file_path)
        except Exception as e:
            print("Error reading DOCX:", e)
    else:
        raise ValueError("Unsupported file format. Only PDF and DOCX allowed.")

    return text

def analyze_resume(text: str, goal: str) -> dict:
    """
    Use AI to find:
    - skills present in resume
    - missing skills based on user's goal
    """
    prompt = f"""
    Analyze the following resume text:

    Resume:
    {text}

    User Goal:
    {goal}

    Task:
    1. List the skills mentioned in the resume.
    2. List the skills the user should have to achieve the goal but are missing in the resume.

    Respond in JSON format:
    {{
        "skills": ["skill1", "skill2", ...],
        "missing_skills": ["skill1", "skill2", ...]
    }}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        content = response.choices[0].message.content

        import json
        result = json.loads(content)
        return result
    except Exception as e:
        print("Error with AI analyze:", e)
        return {"skills": [], "missing_skills": []}
