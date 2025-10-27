import streamlit as st, requests, urllib.parse

st.title("Avaliador de Artigos – PDF")

default_api = "http://127.0.0.1:8000/analyze"
api_url = st.text_input("URL da API (endpoint /analyze)", default_api)
pdf = st.file_uploader("Envie seu PDF", type=["pdf"])

def base_url_from_analyze(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    path = parsed.path
    if path.endswith("/analyze"):
        path = path[: -len("/analyze")] or "/"
    return urllib.parse.urlunparse(parsed._replace(path=path, params="", query="", fragment=""))

if st.button("Testar conexão"):
    try:
        root = base_url_from_analyze(api_url)
        r = requests.get(root, timeout=5)
        st.success(f"Conectado em {root} (status {r.status_code}) → {r.text}")
    except Exception as e:
        st.error(f"Falha ao conectar: {e}")

st.divider()

if st.button("Analisar") and pdf:
    try:
        r = requests.post(api_url, files={"file": (pdf.name, pdf.read(), "application/pdf")}, timeout=120)
        r.raise_for_status()
        resp = r.json()
        st.success("Análise concluída!")

        st.json(resp.get("metrics", {}))
        for tip in resp.get("tips", []):
            st.write(f"- {tip}")
        if resp.get("report_markdown"):
            st.markdown(resp["report_markdown"])
    except Exception as e:
        st.error(f"Erro ao analisar: {e}")
