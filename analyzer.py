from utils_pdf import extract_pdf_text
from rules import compute_metrics, build_advice

def analyze_pdf(file_bytes: bytes) -> dict:
    text = extract_pdf_text(file_bytes)
    metrics = compute_metrics(text)
    tips = build_advice(text, metrics)
    return {
        "metrics": metrics.__dict__,
        "tips": tips,
        "report_markdown": (
            f"# Relatório de Avaliação\n\n"
            f"- Palavras: **{metrics.words}**\n"
            f"- Frases: **{metrics.sentences}**\n"
            f"- Flesch (pt): **{metrics.flesch:.1f}**\n"
            f"- DOIs detectados: **{metrics.dois}**\n"
        )
    }
