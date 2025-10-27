import re
from dataclasses import dataclass
import textstat
import spacy

HEADER_PATTERNS = [
    r"^resumo", r"^abstract", r"^palavras[- ]chave", r"^introdu",
    r"^metodologia|^m[eé]todos", r"^resultados?", r"^discuss",
    r"^conclus", r"^refer"
]

DOI_RE = re.compile(r"10\.\d{4,9}/\S+")

nlp = spacy.load("pt_core_news_sm")
textstat.set_lang("pt")

@dataclass
class Metrics:
    words: int
    sentences: int
    flesch: float
    dois: int
    headers: dict

def detect_headers(text: str):
    lines = [l.strip().lower() for l in text.splitlines() if l.strip()]
    found = {}
    for pat in HEADER_PATTERNS:
        rx = re.compile(pat, re.IGNORECASE)
        found[pat] = any(rx.match(l) for l in lines)
    return found

def compute_metrics(text: str) -> Metrics:
    words = len(re.findall(r"\b\w+\b", text))
    sentences = max(textstat.sentence_count(text), 1)
    flesch = textstat.flesch_reading_ease(text)
    dois = len(DOI_RE.findall(text))
    headers = detect_headers(text)
    return Metrics(words, sentences, flesch, dois, headers)

def build_advice(text: str, m: Metrics):
    tips = []
    if m.flesch < 40:
        tips.append("Texto denso: reduza frases longas e simplifique construções.")
    if not any(m.headers.values()):
        tips.append("Faltam seções estruturais (Resumo, Introdução, Metodologia, Resultados, Discussão, Conclusão, Referências).")
    if m.dois == 0:
        tips.append("Inclua DOIs nas referências quando disponíveis.")
    return tips
