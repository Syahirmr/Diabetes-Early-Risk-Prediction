# Architecture

Project: Diabetes Early Risk Prediction Platform
Version: 1.1

Purpose:
Mendefinisikan arsitektur sistem secara menyeluruh, termasuk struktur komponen, aliran data, tanggung jawab layanan, integrasi, dan aturan operasional.

Consumer:

* Frontend Engineer
* Backend Engineer
* ML Engineer
* DevOps
* Product Owner

Source of Truth:

* docs/system_spec.md
* docs/data_contract.md
* docs/api_contract.md
* docs/ml_pipeline.md
* docs/uiux_spec.md
* docs/decision_log.md

Architecture Style

Decoupled

Stateless

API Driven

Single Model Inference

---

# 1. System Overview

Platform terdiri dari dua aplikasi independen.

Frontend

↓

REST API

↓

Backend AI Engine

↓

Model Artifacts

↓

Prediction Result

---

Goals

* memisahkan presentasi dan inferensi
* mempermudah deployment
* menjaga skalabilitas
* menjaga konsistensi kontrak

---

# 2. High Level Architecture

┌─────────────────────────┐

Frontend Web

(Tailwind + Alpine)

└──────────┬──────────────┘

↓

HTTPS + JSON

↓

┌─────────────────────────┐

Backend API

(FastAPI)

└──────────┬──────────────┘

↓

Application Service

↓

ML Inference Service

↓

Explainability Service

↓

┌─────────────────────────┐

Artifact Registry (RAM)

RF + SHAP

└─────────────────────────┘

---

Responsibilities

Frontend

* rendering
* edukasi
* form interaction
* state UI

Backend

* validation
* orchestration
* formatting

ML Layer

* preprocessing
* prediction
* explainability

---

# 3. Logical Layers

Presentation

↓

Application

↓

Domain

↓

ML

↓

Infrastructure

---

Presentation

frontend/

Responsibilities

* pages
* components
* visualization

---

Application

backend/api

Responsibilities

* routing
* validation
* DTO mapping

---

Domain

backend/services

Responsibilities

* prediction flow
* explainability flow

---

ML

backend/ml

Responsibilities

* transform
* inference
* scoring

---

Infrastructure

infra/

Responsibilities

* deployment
* monitoring
* environment

---

# 4. Component Diagram

Frontend

├── Landing

├── Assessment

├── Result

└── Export

↓

API

↓

Prediction Service

├── Validator

├── Encoder

├── Predictor

└── Explainability

↓

Artifact Registry

├── model.pkl

├── encoder.pkl

├── preprocessor.pkl

├── explainer.pkl

├── metadata.json

└── metrics.json

---

# 5. Repository Structure

root/

docs/

frontend/

backend/

models/

tests/

infra/

scripts/

README.md

---

frontend/

components/

pages/

services/

store/

assets/

---

backend/

api/

services/

schemas/

ml/

utils/

startup/

---

models/

artifacts/

versions/

---

tests/

frontend/

backend/

ml/

integration/

---

# 6. Frontend Architecture

Framework

HTML

Tailwind

Alpine.js

Pattern

Component Driven

---

Responsibilities

Landing

↓

Assessment

↓

Result

↓

Export

---

State

Session Only

Rules

* tidak ada persistence
* tidak ada local database
* state hilang saat refresh

---

Flow

Input

↓

Validate

↓

API Call

↓

Render

---

# 7. Backend Architecture

Framework

FastAPI

Pattern

Service Layer

---

Request

↓

Router

↓

Schema Validation

↓

Prediction Service

↓

ML Service

↓

Response Mapper

↓

JSON

---

Rules

Router tidak boleh berisi business logic.

---

# 8. ML Serving Architecture

Goal

Inference cepat dan konsisten.

---

Application Lifecycle

Server Startup

↓

Load Artifacts

↓

Register to Memory

↓

API Ready

---

Loaded Components

encoder.pkl

preprocessor.pkl

model.pkl

explainer.pkl

metadata.json

---

Artifact Registry

Read Only

Singleton Scope

Memory Resident

---

Request Flow

Receive Request

↓

Validate

↓

Transform

↓

Predict

↓

Explain

↓

Format Response

↓

Return JSON

---

Rules

Artifacts WAJIB di-load saat startup.

Artifacts tidak boleh di-load ulang per request.

Artifacts hanya dibaca.

Tidak boleh retrain saat runtime.

Tidak boleh mengganti artifact tanpa restart.

---

Expected Warmup

< 10 sec

Expected Inference

< 1 sec

---

# 9. Sequence Diagram

User

↓

Frontend

↓

POST /predict

↓

Backend

↓

Validation

↓

Preprocess

↓

Predict

↓

Explain

↓

Response

↓

Render

---

SLA

< 3 sec

---

# 10. Data Flow

User Input

↓

Frontend State

↓

JSON

↓

Backend Validation

↓

Transform

↓

Inference

↓

Explanation

↓

Response DTO

↓

UI

---

Boundaries

Frontend

tidak mengetahui model.

Backend

tidak mengetahui UI.

Model

tidak mengetahui HTTP.

---

# 11. Security Architecture

Transport

HTTPS

---

CORS

restricted

---

Authentication

none

---

Session

none

---

Persistence

none

---

Logging

anonymous

---

Forbidden

* data klinis mentah
* identitas user

---

# 12. Availability

Target

99%

Recovery

restart service

Timeout

3 sec

---

Fallback

Prediction Fail

↓

friendly error

---

Explainability Fail

↓

return prediction only

---

# 13. Observability

Metrics

* latency
* health
* error_rate
* prediction_count
* drift

---

Endpoints

/health

/metadata

---

Logs

structured

---

Alert

latency > 3 sec

error > 5%

---

# 14. Deployment Architecture

Frontend

Static Hosting

↓

Backend

Container

↓

Artifact Volume

Mounted Read Only

---

Environment

DEV

STAGING

PRODUCTION

---

Environment Variables

MODEL_PATH

API_BASE_URL

ALLOWED_ORIGINS

APP_ENV

---

# 15. Scalability Rules

Frontend

horizontal

---

Backend

horizontal

---

Artifacts

shared immutable

---

Model

single active version

---

Autoscaling

future

---

# 16. Failure Strategy

Validation

422

---

Prediction

500

---

Network

retry

---

Explainability

fallback

---

Startup Fail

abort boot

---

# 17. Non Functional Requirements

Warmup

< 10 sec

---

Inference

< 1 sec

---

Availability

99%

---

Accessibility

WCAG AA

---

Mobile First

required

---

# 18. Architecture Constraints

Tidak boleh:

* training di production
* inference tanpa validasi
* load artifact per request
* menyimpan data pasien
* modifikasi artifact runtime
* menampilkan output teknis ke user

---

# 19. Ownership

Frontend

UI

Backend

API

ML

Inference

DevOps

Deployment

Perubahan arsitektur wajib update:

* architecture.md
* system_spec.md
* api_contract.md
* decision_log.md
