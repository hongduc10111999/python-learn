import os

os.environ.setdefault("PYTHONWARNINGS", "ignore")
os.environ.setdefault("GRPC_VERBOSITY", "ERROR")
os.environ.setdefault("GLOG_minloglevel", "2")

import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

import google.generativeai as genai
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "models/text-embedding-004")

CHROMA_DIR = str(BASE_DIR / "chroma_db")


def require_api_key():
    if not GEMINI_API_KEY:
        raise SystemExit(
            "Thiếu GEMINI_API_KEY. Hãy copy .env.example thành .env và điền API key.\n"
            "Lấy key miễn phí tại: https://aistudio.google.com/apikey"
        )
    genai.configure(api_key=GEMINI_API_KEY)
