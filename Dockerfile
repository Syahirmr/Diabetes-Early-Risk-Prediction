FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin kode Backend (Tanpa artefak model biner yang besar, di-mount via Volume)
COPY backend/ ./backend/
COPY scripts/ ./scripts/

# Menjalankan FastAPI dengan 4 workers untuk mendistribusikan beban CPU SHAP
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
