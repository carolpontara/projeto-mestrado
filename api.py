import logging
import os

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader

from analyzer import analyze_pdf
from analyzer_llm import analyze_llm

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration via environment variables
# ---------------------------------------------------------------------------
ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "").split(",")
ALLOWED_ORIGINS = [o.strip() for o in ALLOWED_ORIGINS if o.strip()]
API_KEY = os.environ.get("API_KEY")  # None disables auth in dev
MAX_UPLOAD_BYTES = int(os.environ.get("MAX_UPLOAD_BYTES", str(10 * 1024 * 1024)))  # 10 MB
DEBUG_MODE = os.environ.get("DEBUG", "false").lower() == "true"

# ---------------------------------------------------------------------------
# App initialisation — disable OpenAPI docs in production
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Avaliador de Artigos (PDF)",
    docs_url="/docs" if DEBUG_MODE else None,
    redoc_url="/redoc" if DEBUG_MODE else None,
    openapi_url="/openapi.json" if DEBUG_MODE else None,
)

# ---------------------------------------------------------------------------
# CORS — allow only explicitly listed origins (deny-all by default)
# ---------------------------------------------------------------------------
if ALLOWED_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["Authorization", "Content-Type"],
    )

# ---------------------------------------------------------------------------
# Authentication dependency
# ---------------------------------------------------------------------------
_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(key: str = Depends(_api_key_header)):
    """Require a valid API key when API_KEY env var is set."""
    if API_KEY is None:
        return  # auth disabled (local dev)
    if not key or key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key.")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
PDF_MAGIC = b"%PDF"


def _validate_pdf(file: UploadFile, content: bytes) -> None:
    """Validate that the upload is actually a PDF (magic-byte check)."""
    if file.content_type not in ("application/pdf",):
        raise HTTPException(400, "Envie um arquivo PDF.")
    if not content[:4].startswith(PDF_MAGIC):
        raise HTTPException(400, "O arquivo enviado nao e um PDF valido.")
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            413,
            f"Arquivo excede o limite de {MAX_UPLOAD_BYTES // (1024 * 1024)} MB.",
        )


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/analyze_spacy")
async def analyze(
    file: UploadFile = File(...),
    _auth: None = Depends(verify_api_key),
):
    pdf_bytes = await file.read()
    _validate_pdf(file, pdf_bytes)
    try:
        result = analyze_pdf(pdf_bytes)
        return JSONResponse(result)
    except Exception:
        logger.exception("Falha na analise spaCy")
        raise HTTPException(500, "Erro interno ao processar o artigo.")


@app.post("/analyze_llm")
async def analyze_llm_router(
    file: UploadFile = File(...),
    _auth: None = Depends(verify_api_key),
):
    pdf_bytes = await file.read()
    _validate_pdf(file, pdf_bytes)
    try:
        result = analyze_llm(pdf_bytes)
        return JSONResponse(result)
    except Exception:
        logger.exception("Falha na analise LLM")
        raise HTTPException(500, "Erro interno ao processar o artigo.")
