# Timeline Execution

Project: Diabetes Early Risk Prediction Platform
Version: 1.1

Purpose:
Menentukan urutan implementasi proyek agar pengembangan berjalan terstruktur, minim rework, dan siap diintegrasikan.

Consumer:

* Product Owner
* Developer
* AI Agent

Source of Truth:

* docs/system_spec.md
* docs/data_contract.md
* docs/api_contract.md
* docs/ml_pipeline.md
* docs/uiux_spec.md
* docs/architecture.md
* docs/prompt_rules.md
* docs/decision_log.md

Execution Philosophy

Build Foundation

↓

Validate Early

↓

Integrate Continuously

↓

Optimize Last

↓

Release Safely

---

Success Definition

Sistem mampu:

* menerima input
* melakukan prediksi
* menjelaskan hasil
* menampilkan hasil
* berjalan stabil

Target

Single Working Release

---

# Phase 0 — Project Bootstrap

Duration

0.5–1 Hari

Goal

Membuat fondasi proyek yang stabil.

Tasks

Create Structure

root/

docs/

frontend/

backend/

models/

tests/

infra/

scripts/

---

Setup Environment

Python

Node

Git

Virtual Env

---

Dependency Lock

WAJIB dibuat:

requirements.txt

pyproject.toml

.env.example

---

Freeze Version

Contoh

python==3.12

fastapi==0.116.*

scikit-learn==1.7.*

pandas==2.3.*

numpy==2.3.*

shap==0.49.*

---

Install Core Packages

Backend

fastapi

uvicorn

pandas

numpy

scikit-learn

shap

imbalanced-learn

joblib

pydantic

---

Frontend

tailwind

alpine

---

Deliverables

repo siap

folder siap

dependency terkunci

---

Exit Criteria

environment berjalan.

---

# Phase 1 — Dataset & Validation

Duration

1–2 Hari

Goal

Dataset siap training.

Tasks

Load Dataset

↓

Audit Kolom

↓

Drop

year

location

clinical_notes

race:*

↓

Type Validation

↓

EDA

↓

Train Test Split

↓

Data Contract Check

---

Output

dataset_clean.csv

eda_summary.md

---

Exit Criteria

tidak ada leakage.

---

# Phase 2 — ML Pipeline

Duration

2–4 Hari

Goal

Menghasilkan artifact produksi.

Tasks

Preprocess

↓

Encoding

↓

SMOTE

↓

Train RF

↓

Evaluate

↓

Generate SHAP

↓

Export

---

Artifacts

model.pkl

encoder.pkl

preprocessor.pkl

explainer.pkl

metadata.json

metrics.json

---

Target

Recall tinggi

Inference cepat

---

Exit Criteria

artifact valid.

---

# Phase 3 — Backend API

Duration

2 Hari

Goal

Backend siap diakses.

Tasks

FastAPI

↓

Schema

↓

Startup Loader

↓

Predict Service

↓

Formatter

↓

Error Handler

↓

Health Endpoint

---

Endpoints

/health

/predict

/explain

/metadata

---

Early Integration (WAJIB)

Postman

↓

curl

↓

browser fetch

↓

Frontend ping

---

CORS Setup

Allow Origin

Environment Driven

---

Deliverables

backend online

swagger aktif

---

Exit Criteria

frontend berhasil request.

---

# Phase 4 — Frontend UI

Duration

2–3 Hari

Goal

User dapat menggunakan aplikasi.

Tasks

Landing

↓

Assessment

↓

Result

↓

Explainability

↓

Export

---

Implement

State

↓

API Client

↓

Loading

↓

Error

↓

Retry

---

Early Connection

Frontend langsung memakai API nyata.

Mock API hanya fallback.

---

Exit Criteria

flow berjalan.

---

# Phase 5 — Integration

Duration

1–2 Hari

Goal

Seluruh sistem terhubung.

Tasks

Response Mapping

↓

Error Mapping

↓

Cross Browser

↓

Mobile

↓

Accessibility

---

Scenario

Success

Validation

Timeout

Backend Down

Explain Fail

---

Exit Criteria

E2E pass.

---

# Phase 6 — Stabilization

Duration

1–2 Hari

Goal

Mencari bug tersembunyi.

Tasks

Profiling

↓

Observability

↓

Logging

↓

Cleanup

↓

Hardening

---

Stress Test

50 request

100 request

burst test

---

Edge Cases

umur ekstrem

angka kosong

nilai negatif

payload rusak

nilai sangat tinggi

---

Failure Cases

422

429

500

---

Observe

latency

memory

CPU

warmup

---

Target

warmup <10 sec

inference <1 sec

response <3 sec

---

Exit Criteria

tidak ada crash.

---

# Phase 7 — Release Candidate

Duration

1 Hari

Goal

Release pertama.

Tasks

Version

↓

Build

↓

Deploy

↓

Smoke Test

↓

Release Notes

---

Output

v1.0

---

Exit Criteria

URL aktif.

---

# Daily Workflow

Pull

↓

Implement

↓

Test

↓

Document

↓

Commit

↓

Push

---

Rule

Tidak boleh coding tanpa update docs.

---

# Branch Strategy

main

stable

---

develop

active

---

feature/*

isolated

---

Merge Rule

tests pass

docs updated

review complete

---

# Definition of Done

Code

PASS

---

Tests

PASS

---

Docs

UPDATED

---

API

VALID

---

UI

COMPLETE

---

Model

LOCKED

---

Performance

PASS

---

# Risk Register

Risk

dependency conflict

Mitigation

freeze version

---

Risk

cors issue

Mitigation

early integration

---

Risk

frontend delay

Mitigation

mock API

---

Risk

data leakage

Mitigation

split first

---

Risk

slow explainability

Mitigation

cache explainer

---

Risk

memory issue

Mitigation

stress test

---

# Deliverables

frontend/

backend/

models/

tests/

docs/

README.md

demo.mp4

release.zip

---

# Final Gate

Checklist

dataset siap

artifact valid

API hidup

UI jalan

respons benar

dokumen sinkron

release siap

---

Estimated Total

10–16 Hari

Solo Development

AI Assisted
