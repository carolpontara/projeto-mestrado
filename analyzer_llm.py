from utils_pdf import extract_pdf_text
from google import genai
import json

from os import environ

def analyze_llm(file_bytes: bytes) -> dict:
    text = extract_pdf_text(file_bytes)
    prompt = f"""
    Analise o artigo abaixo e retorne um JSON com:

    - resumo
    - tópicos principais
    - entidades importantes
    - tom do texto

    Texto:
    \"\"\"{text}\"\"\"
    """

    client = genai.Client(api_key=environ['api_key_llm'])
    response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=prompt
    )

    response = response.text.replace("json","")
    response = response.replace("```","")
    return json.loads(response)