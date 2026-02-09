import os
from fastapi import APIRouter
from app.vector_store.faiss_index import index, metadata_store

router = APIRouter(prefix="/debug", tags=["Debug"])

_SAFE_ENV_KEYS = {
    "PORT",
    "ALLOWED_ORIGINS",
    "FIREBASE_STORAGE_BUCKET",
    "RENDER",
    "RENDER_SERVICE_ID",
    "RENDER_SERVICE_NAME",
    "RENDER_EXTERNAL_URL",
    "RENDER_INSTANCE_ID",
    "PYTHON_VERSION",
}

def _safe_env():
    data = {}
    for key in _SAFE_ENV_KEYS:
        value = os.getenv(key)
        if value is not None:
            data[key] = value
    return data

@router.get("/vector-count")
def vector_count():
    return {
        "faiss_vectors": int(index.ntotal),
        "metadata_entries": len(metadata_store),
    }

@router.get("/env")
def env():
    return _safe_env()
