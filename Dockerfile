FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ARG SPACY_MODEL=pt_core_news_sm
RUN python -m spacy download ${SPACY_MODEL}

COPY . .

EXPOSE ${API_PORT:-8000}

CMD ["sh", "-c", "uvicorn api:app --host ${API_HOST:-0.0.0.0} --port ${API_PORT:-8000}"]
