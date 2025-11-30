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

def render_report(metrics, spacy_info):
    md = []

    md.append("# 📊 Relatório de Análise do Artigo\n")

    # --- Estatísticas básicas ---
    md.append("## 📈 Métricas Gerais")
    md.append(f"- **Palavras:** {metrics.words}")
    md.append(f"- **Frases:** {metrics.sentences}")
    md.append(f"- **Flesch (pt):** {metrics.flesch:.1f}")
    md.append(f"- **DOIs detectados:** {metrics.dois}")

    # --- Estrutura detectada ---
    md.append("\n## 🧩 Estrutura do Artigo")
    for section, exists in metrics.headers.items():
        md.append(f"- {section}: {'✔️' if exists else '❌'}")

    # --- Entidades spaCy ---
    md.append("\n## 🏷️ Entidades Nomeadas Detectadas (spaCy)")
    if spacy_info["entities"]:
        for text, label in spacy_info["entities"][:30]:
            md.append(f"- `{text}` — **{label}**")
    else:
        md.append("_Nenhuma entidade detectada._")

    # --- Keywords ---
    md.append("\n## 🔑 Palavras-chave (Lemmatizadas)")
    if spacy_info["keywords"]:
        keywords_str = ", ".join(spacy_info["keywords"])
        md.append(keywords_str)
    else:
        md.append("_Nenhuma palavra-chave encontrada._")

    # --- Contagens ---
    md.append("\n## 📊 Resumo da Análise Linguística")
    md.append(f"- **Total de entidades:** {spacy_info['num_entities']}")
    md.append(f"- **Keywords únicas:** {spacy_info['num_unique_keywords']}")

    return "\n".join(md)