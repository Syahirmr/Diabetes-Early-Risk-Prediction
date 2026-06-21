# 🩺 Diabetes Early Risk Prediction Platform

![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?logo=fastapi&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-5.4%2B-646CFF?logo=vite&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.4-38B2AC?logo=tailwind-css&logoColor=white)
![Machine Learning](https://img.shields.io/badge/ML-Random_Forest-FF6F00?logo=scikit-learn&logoColor=white)

Sebuah platform web berbasis *Machine Learning* yang memprediksi risiko awal diabetes pada pasien berdasarkan data klinis dan gaya hidup. Sistem ini tidak hanya memberikan probabilitas risiko, tetapi juga menyediakan **Explainable AI (XAI)** menggunakan algoritma **SHAP (SHapley Additive exPlanations)** agar dokter/pasien dapat memahami faktor spesifik apa yang memicu tingginya risiko tersebut.

---

## ✨ Fitur Utama

- **Real-time Inference API:** Backend super cepat berbasis `FastAPI` dengan perlindungan *Fail-Fast* dan *Data Contract Validation* via Pydantic.
- **Explainable AI (SHAP):** Secara otomatis menjabarkan kontribusi positif dan negatif setiap metrik pasien (umur, HbA1c, glukosa darah, BMI, dll) terhadap hasil prediksi.
- **Dynamic Thresholding & SMOTE:** Menangani ketidakseimbangan data (imbalanced dataset) agar metrik **Recall** dapat diandalkan secara medis.
- **Production-Ready Frontend:** SPA (Single Page Application) super ringan yang di-bundle menggunakan `Vite`, di-styling menggunakan `Tailwind CSS`, dan menggunakan `Alpine.js` untuk reaktivitas *state*.
- **Comprehensive E2E Testing:** Dilindungi dengan pengujian *End-to-End* menggunakan **Playwright** dan pengujian API menggunakan **Pytest**.

---

## 🏗️ Arsitektur Sistem

- **Frontend**: Vite + Alpine.js + TailwindCSS + ES Modules (Tanpa Framework Heavyweight).
- **Backend**: FastAPI + Uvicorn + Pydantic (Validasi Strict).
- **ML Pipeline**: Scikit-Learn (Random Forest) + Imbalanced-Learn (SMOTE) + SHAP.

---

## 🚀 Persiapan & Instalasi (Getting Started)

Karena *repository* ini dijaga agar 100% *clean* dari file data yang sangat besar dan *artifact* ML berukuran raksasa, **Anda diwajibkan untuk men-generate modelnya sendiri secara lokal setelah melakukan clone**. 

Ikuti instruksi berikut dengan teliti:

### 1. Clone Repository & Environment
```bash
git clone https://github.com/Syahirmr/Diabetes-Early-Risk-Prediction.git
cd Diabetes-Early-Risk-Prediction

# (Opsional) Buat virtual environment
python -m venv .venv
# Windows:
.\.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
# Install seluruh library Python (termasuk dev dependencies)
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install package Node.js untuk Frontend bundler
npm install
```

### 3. Generate ML Artifacts (WAJIB DILAKUKAN) ⚠️
Jika langkah ini dilewati, backend server **akan langsung crash (Fail-Fast)** karena tidak menemukan file model. Siapkan `data/diabetes_dataset_with_notes.csv` (hubungi *author* untuk dataset) atau jalankan pipeline menggunakan dataset lokal Anda.

Jika data lokal sudah tersedia di direktori, bangun ulang *model artifact* `.pkl` dengan cara:
```bash
python scripts/phase2_pipeline.py
```
*(Script ini akan memproses dataset, melatih Random Forest, men-generate explainer, dan menaruh seluruh model ke folder `models/artifacts/`)*.

---

## 💻 Menjalankan Aplikasi

Aplikasi berjalan pada arsitektur terpisah untuk *development* (Frontend di port 3000, Backend di port 8000).

### 1. Jalankan FastAPI Backend
```bash
uvicorn backend.main:app --reload
```
- API Endpoint: `http://localhost:8000/api/v1/predict`
- Swagger UI (Dokumentasi API): `http://localhost:8000/docs`

### 2. Jalankan Vite Frontend Server
Buka terminal baru, dan pastikan berada di folder project:
```bash
npm run dev
```
- UI Platform siap diakses di: **`http://localhost:3000`**

### 3. Production Build (Opsional)
Untuk mengemas frontend dan langsung mengintegrasikannya dengan kode statik:
```bash
npm run build
```

---

## 🧪 Validasi & Testing

Sistem ini memiliki pipeline pengujian (E2E & Backend) yang kuat:

```bash
# Run seluruh tes API Backend (Pytest)
pytest

# Linter & Type Checkers
ruff check .
mypy backend

# Run UI E2E Test Browser (Playwright)
npx playwright test
# Atau jalankan script orkestrasi otomatis kami:
python scripts/run_e2e.py
```

---

## 📂 Struktur Direktori

```text
Diabetes-Early-Risk-Prediction/
├── backend/            # FastAPI, Router, Schema, Logic Inference
├── docs/               # Spesifikasi Sistem & Kontrak Data
├── frontend/           # Aplikasi Web SPA (Alpine.js + Tailwind)
├── models/artifacts/   # Tempat hasil build model (*Diabaikan oleh git*)
├── reports/            # Markdown laporan validasi otomatis dari Script & Test
├── scripts/            # Pipeline Training, ML Ops, & Utility Scaffolding
└── tests/              # E2E Playwright & Pytest
```

---
*Dibuat untuk Tugas Akhir/Proyek Pembelajaran Mesin Universitas.* 
**Disclaimer**: Ini bukan alat diagnostik medis sungguhan. Konsultasikan dengan tenaga medis profesional.
