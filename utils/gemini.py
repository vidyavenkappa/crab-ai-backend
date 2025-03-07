import google.generativeai as genai
import os

# Set your Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def validate_paper_with_gemini(file_path):
    """
    Uses Gemini AI to analyze and validate the uploaded paper.
    Returns a summary and an AI-generated score.
    """
    with open(file_path, "rb") as pdf_file:
        document = pdf_file.read()

    # Call Gemini API (mock response for now)
    response = genai.generate_content(prompt="Analyze and summarize this research paper. Return output in form of a json :{'summary':'summary text', 'score':'score of the text'}", files=[document])

    # Extract AI review summary and score (Mock values)
    summary = response.get("summary", "AI review not available.")
    score = response.get("score", 7.5)  # Default score if not provided

    return {
        "summary": summary,
        "score": score
    }
