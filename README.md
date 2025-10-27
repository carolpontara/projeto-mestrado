# Avaliador de Artigos (PDF)

## Como rodar local
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m spacy download pt_core_news_sm
uvicorn api:app --reload --port 8000
```

Depois envie um PDF para `http://localhost:8000/analyze` via Postman ou cURL.
```bash
curl -X POST -F "file=@meuartigo.pdf" http://localhost:8000/analyze
```
