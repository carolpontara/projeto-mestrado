import logging
from os import environ

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader

from analyzer import analyze_pdf
from analyzer_llm import analyze_llm

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = FastAPI(title="Avaliador de Artigos (PDF)")

# ---------------------------------------------------------------------------
# CORS – restrict origins; override with CORS_ORIGINS env var (comma-sep)
# ---------------------------------------------------------------------------
_default_origins = ["http://localhost:8501", "http://127.0.0.1:8501"]
_origins = [
    o.strip()
    for o in environ.get("CORS_ORIGINS", "").split(",")
    if o.strip()
] or _default_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Optional API-key auth – enabled when API_KEY env var is set
# ---------------------------------------------------------------------------
_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(api_key: str = Depends(_api_key_header)):
    expected = environ.get("API_KEY")
    if expected and api_key != expected:
        raise HTTPException(status_code=403, detail="Invalid or missing API key.")


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
MAX_UPLOAD_BYTES = 10 * 1024 * 1024  # 10 MB
PDF_MAGIC = b"%PDF"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _validate_pdf(pdf_bytes: bytes, content_type: str) -> None:
    """Validate both Content-Type and magic bytes."""
    if content_type not in ("application/pdf",):
        raise HTTPException(400, "Envie um arquivo PDF.")
    if not pdf_bytes[:4].startswith(PDF_MAGIC):
        raise HTTPException(400, "O arquivo não parece ser um PDF válido.")


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/")
def health():
    return {"status": "ok", "endpoints": ["/analyze_spacy (POST)", "/analyze_llm (POST)"]}


@app.get("/analyze")
def analyze_get_help():
    return {
        "message": "Use POST multipart/form-data em /analyze_spacy ou /analyze_llm com o campo 'file' contendo o PDF.",
        "example_curl": 'curl -X POST -F "file=@meu.pdf" http://127.0.0.1:8000/analyze_spacy',
    }


@app.post("/analyze_spacy")
async def analyze(
    file: UploadFile = File(...),
    _key: str = Depends(verify_api_key),
):
    pdf_bytes = await file.read(MAX_UPLOAD_BYTES + 1)
    if len(pdf_bytes) > MAX_UPLOAD_BYTES:
        raise HTTPException(413, "Arquivo excede o limite de 10 MB.")
    _validate_pdf(pdf_bytes, file.content_type)
    try:
        result = analyze_pdf(pdf_bytes)
        return JSONResponse(result)
    except Exception:
        logger.exception("Error in /analyze_spacy")
        raise HTTPException(500, "Erro interno ao processar o artigo.")


@app.post("/analyze_llm")
async def analyze_llm_router(
    file: UploadFile = File(...),
    _key: str = Depends(verify_api_key),
):
    pdf_bytes = await file.read(MAX_UPLOAD_BYTES + 1)
    if len(pdf_bytes) > MAX_UPLOAD_BYTES:
        raise HTTPException(413, "Arquivo excede o limite de 10 MB.")
    _validate_pdf(pdf_bytes, file.content_type)
    try:
        result = analyze_llm(pdf_bytes)
        return JSONResponse(result)
    except Exception:
        logger.exception("Error in /analyze_llm")
        raise HTTPException(500, "Erro interno ao processar o artigo.")
