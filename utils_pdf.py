import fitz  # PyMuPDF

def extract_pdf_text(path_or_bytes: bytes | str) -> str:
    doc = fitz.open(stream=path_or_bytes, filetype="pdf") if isinstance(path_or_bytes, (bytes, bytearray)) else fitz.open(path_or_bytes)
    texts = []
    for page in doc:
        blocks = page.get_text("blocks")
        blocks = sorted(blocks, key=lambda b: (b[1], b[0]))
        page_text = "\n".join(b[4] for b in blocks if b[4].strip())
        texts.append(page_text)
    return "\n\n".join(texts)
