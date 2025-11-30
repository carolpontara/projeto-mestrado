from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from analyzer import analyze_pdf
from analyzer_llm import analyze_llm

app = FastAPI(title="Avaliador de Artigos (PDF)")

@app.get("/")
def health():
    return {"status": "ok", "endpoints": ["/analyze (POST multipart)"]}

@app.get("/analyze")
def analyze_get_help():
    return {
        "message": "Use POST multipart/form-data em /analyze com o campo 'file' contendo o PDF.",
        "example_curl": 'curl -X POST -F "file=@meu.pdf" http://127.0.0.1:8000/analyze'
    }

@app.post("/analyze_spacy")
async def analyze(file: UploadFile = File(...)):
    if file.content_type not in ("application/pdf",):
        raise HTTPException(400, "Envie um arquivo PDF.")
    pdf_bytes = await file.read()
    try:
        result = analyze_pdf(pdf_bytes)
        return JSONResponse(result)
    except Exception as e:
        raise HTTPException(500, f"Falha na análise: {e}")


@app.post("/analyze_llm")
async def analyze_llm_router(file: UploadFile = File(...)):
    if file.content_type not in ("application/pdf",):
        raise HTTPException(400, "Envie um arquivo PDF.")
    pdf_bytes = await file.read()
    try:
        result = analyze_llm(pdf_bytes)
        return JSONResponse(result)
    except Exception as e:
        raise HTTPException(500, f"Falha na análise: {e}")
