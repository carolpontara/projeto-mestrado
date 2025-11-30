from utils_pdf import extract_pdf_text, render_report
from rules import compute_metrics, build_advice, analyze_with_spacy

def analyze_pdf(file_bytes: bytes) -> dict:
    text = extract_pdf_text(file_bytes)
    metrics = compute_metrics(text)
    tips = build_advice(text, metrics)
    nlp_info = analyze_with_spacy(text)

    return {
        "metrics": metrics.__dict__,
        "tips": tips,
        "report_markdown": render_report(metrics, nlp_info)
    }
