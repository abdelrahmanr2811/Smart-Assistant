import os
import re
import time
from pathlib import Path
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import httpx

from app.config import settings

router = APIRouter(prefix="/settings", tags=["System & LLM Settings"])

class GeminiSettingsPayload(BaseModel):
    gemini_api_key: str
    gemini_model: Optional[str] = None

class GeminiTestPayload(BaseModel):
    gemini_api_key: Optional[str] = None
    gemini_model: Optional[str] = None

def _persist_env_key(key_name: str, key_val: str):
    """Safely updates or appends a key in backend/.env file and root .env."""
    env_paths = [
        Path(__file__).resolve().parent.parent.parent / ".env",       # backend/.env
        Path(__file__).resolve().parent.parent.parent.parent / ".env" # root .env
    ]
    for env_path in env_paths:
        try:
            if not env_path.exists():
                with open(env_path, "w", encoding="utf-8") as f:
                    f.write(f"{key_name}={key_val}\n")
                continue
            
            with open(env_path, "r", encoding="utf-8") as f:
                content = f.read()

            pattern = rf"^{key_name}=.*$"
            if re.search(pattern, content, flags=re.MULTILINE):
                new_content = re.sub(pattern, f"{key_name}={key_val}", content, flags=re.MULTILINE)
            else:
                new_content = content.rstrip() + f"\n{key_name}={key_val}\n"

            with open(env_path, "w", encoding="utf-8") as f:
                f.write(new_content)
        except Exception as e:
            print(f"Warning: could not update env file at {env_path}: {e}")

@router.get("/gemini", response_model=Dict[str, Any])
def get_gemini_settings():
    """Returns current Gemini API key, model, and configuration status."""
    key = settings.GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY", "")
    masked = ""
    if key:
        if len(key) > 10:
            masked = key[:6] + "..." + key[-4:]
        else:
            masked = "••••••••"
    
    return {
        "gemini_api_key": key,
        "masked_key": masked,
        "gemini_model": settings.GEMINI_MODEL or os.environ.get("GEMINI_MODEL", "gemini-2.5-flash"),
        "is_configured": bool(key and len(key.strip()) > 5),
        "provider": settings.LLM_PROVIDER
    }

@router.post("/gemini", response_model=Dict[str, Any])
def update_gemini_settings(payload: GeminiSettingsPayload):
    """Updates runtime Gemini API key and model and persists them to .env."""
    new_key = payload.gemini_api_key.strip()
    if not new_key:
        raise HTTPException(status_code=400, detail="Gemini API Key cannot be empty.")

    # 1. Update in-memory configuration
    settings.GEMINI_API_KEY = new_key
    os.environ["GEMINI_API_KEY"] = new_key

    if payload.gemini_model:
        m = payload.gemini_model.strip()
        settings.GEMINI_MODEL = m
        os.environ["GEMINI_MODEL"] = m

    # 2. Persist to .env files
    _persist_env_key("GEMINI_API_KEY", new_key)
    if payload.gemini_model:
        _persist_env_key("GEMINI_MODEL", payload.gemini_model.strip())

    return {
        "status": "success",
        "message": "Gemini API key updated successfully and saved to configuration.",
        "gemini_api_key": new_key,
        "gemini_model": settings.GEMINI_MODEL,
        "is_configured": True
    }

@router.post("/gemini/test", response_model=Dict[str, Any])
def test_gemini_connection(payload: Optional[GeminiTestPayload] = None):
    """Tests live connection to Google Gemini Generative Language API."""
    if payload and payload.gemini_api_key is not None:
        key = payload.gemini_api_key.strip()
    else:
        key = (settings.GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY", "")).strip()

    if payload and payload.gemini_model is not None and payload.gemini_model.strip():
        model = payload.gemini_model.strip()
    else:
        model = settings.GEMINI_MODEL or os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
    clean_model = model.replace("models/", "")

    if not key or len(key.strip()) < 5:
        return {
            "status": "error",
            "message": "No valid Gemini API key configured to test. Please enter a key.",
            "latency_ms": 0
        }

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{clean_model}:generateContent?key={key}"
    start_time = time.time()
    try:
        req_body = {
            "contents": [
                {
                    "parts": [{"text": "Ping test for Smart Project Manager Assistant SPMA. Reply with OK."}]
                }
            ],
            "generationConfig": {
                "maxOutputTokens": 10,
                "temperature": 0.1
            }
        }
        with httpx.Client(timeout=10.0) as client:
            resp = client.post(url, json=req_body)
            latency_ms = int((time.time() - start_time) * 1000)

            if resp.status_code == 200:
                data = resp.json()
                reply = "Operational (200 OK)"
                try:
                    reply = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                except Exception:
                    pass
                return {
                    "status": "success",
                    "message": f"Connection Successful! Gemini API responded in {latency_ms}ms.",
                    "latency_ms": latency_ms,
                    "model": clean_model,
                    "reply": reply
                }
            else:
                err_msg = resp.text
                try:
                    err_json = resp.json()
                    err_msg = err_json.get("error", {}).get("message", resp.text)
                except Exception:
                    pass

                if resp.status_code == 429:
                    return {
                        "status": "error",
                        "error_code": "QUOTA_EXCEEDED",
                        "message": f"Quota Exceeded (429): Google's free-tier quota for '{clean_model}' was reached (20 requests/day). Paste a fresh free key from Google AI Studio or change model.",
                        "raw_error": err_msg,
                        "latency_ms": latency_ms
                    }

                return {
                    "status": "error",
                    "message": f"API Error ({resp.status_code}): {err_msg}",
                    "latency_ms": latency_ms
                }
    except Exception as e:
        latency_ms = int((time.time() - start_time) * 1000)
        return {
            "status": "error",
            "message": f"Connection Failed: {str(e)}",
            "latency_ms": latency_ms
        }
