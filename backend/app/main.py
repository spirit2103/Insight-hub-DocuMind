import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import upload, documents, metadata, charts, qa, debug

app = FastAPI(title="InsightHub Backend")
logger = logging.getLogger("insight-hub")

def _get_allowed_origins():
    raw = os.getenv("ALLOWED_ORIGINS", "")
    if raw:
        return [o.strip() for o in raw.split(",") if o.strip()]
    return [
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(documents.router)
app.include_router(metadata.router)
app.include_router(charts.router)
app.include_router(qa.router)
app.include_router(debug.router)

@app.on_event("startup")
def _log_startup():
    port = os.getenv("PORT", "8000")
    logger.info("Starting InsightHub Backend on port %s", port)

@app.get("/")
def health():
    return {"status": "Backend running"}
