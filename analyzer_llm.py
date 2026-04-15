import json
import logging
import os
import re

from google import genai

from utils_pdf import extract_pdf_text

logger = logging.getLogger(__name__)

_MAX_TEXT_CHARS = 100_000  # truncate very large documents before sending to LLM


def _sanitize_for_prompt(text: str) -> str:
    """Basic sanitisation: strip triple-quote sequences and limit length."""
    text = text.replace('"""', '"\u201d"')
    if len(text) > _MAX_TEXT_CHARS:
        text = text[:_MAX_TEXT_CHARS] + "\n[texto truncado]"
    return text


def _get_api_key() -> str:
    key = os.environ.get("API_KEY_LLM", "")
    if not key:
        raise RuntimeError(
            "A variavel de ambiente API_KEY_LLM nao esta definida. "
            "Configure-a antes de usar o endpoint /analyze_llm."
        )
    return key


def analyze_llm(file_bytes: bytes) -> dict:
    text = extract_pdf_text(file_bytes)
    sanitized = _sanitize_for_prompt(text)

    prompt = (
        "Analise o artigo abaixo e retorne SOMENTE um JSON valido com os campos:\n"
        "- resumo\n- topicos_principais\n- entidades_importantes\n- tom_do_texto\n\n"
        "Texto:\n"
        f"{sanitized}\n"
    )

    client = genai.Client(api_key=_get_api_key())
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    raw = response.text
    # Strip markdown code fences the model may wrap the JSON in
    raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.MULTILINE)
    raw = re.sub(r"```\s*$", "", raw, flags=re.MULTILINE)
    return json.loads(raw.strip())
