# Decision Log

Project: Diabetes Early Risk Prediction Platform
Version: 1.0

Purpose:
Mencatat keputusan desain, teknis, dan produk agar proyek tetap konsisten dan dapat ditelusuri.

Consumer:

* Product Owner
* Frontend Engineer
* Backend Engineer
* ML Engineer
* Researcher

Source of Truth:

* docs/system_spec.md
* docs/data_contract.md
* docs/api_contract.md
* docs/ml_pipeline.md
* docs/uiux_spec.md

Status Legend:

PROPOSED

ACCEPTED

DEPRECATED

REJECTED

SUPERSEDED

---

# ADR-001

Title

Decoupled Architecture

Date

2026-06-21

Status

ACCEPTED

Decision

Frontend dan backend dipisahkan.

Frontend fokus pada edukasi dan interaksi.

Backend fokus pada inference.

Context

Perubahan UI tidak boleh memengaruhi model.

Alternatives

Monolithic App

Rejected Because

Sulit dipelihara.

Consequences

* scalable

* deployment independen

− integrasi lebih kompleks

---

# ADR-002

Title

Model Selection

Date

2026-06-21

Status

ACCEPTED

Decision

Menggunakan Random Forest.

Context

Model perlu stabil dan memiliki performa tinggi.

Alternatives

Logistic Regression

XGBoost

SVM

Rejected Because

Logistic:
lebih sederhana namun performa awal lebih rendah.

XGBoost:
lebih kompleks.

SVM:
kurang efisien untuk deployment.

Consequences

* performa baik

* cocok untuk SHAP

− interpretasi langsung terbatas

---

# ADR-003

Title

Imbalanced Handling

Date

2026-06-21

Status

ACCEPTED

Decision

SMOTE digunakan hanya pada training.

Context

Distribusi kelas tidak seimbang.

Alternatives

Random Oversampling

Undersampling

Class Weight Only

Rejected Because

oversampling:
duplikasi data.

undersampling:
kehilangan informasi.

Consequences

* recall meningkat

− potensi overfitting

---

# ADR-004

Title

Primary Metric

Date

2026-06-21

Status

ACCEPTED

Decision

Recall menjadi metrik utama.

Context

False Negative lebih berisiko.

Alternatives

Accuracy

Precision

ROC-AUC

Rejected Because

accuracy menyesatkan pada data imbalance.

Consequences

* deteksi lebih sensitif

− false positive dapat meningkat

---

# ADR-005

Title

Explainability Strategy

Date

2026-06-21

Status

ACCEPTED

Decision

Menggunakan SHAP.

Context

Prediksi perlu dapat dijelaskan.

Alternatives

LIME

Permutation Importance

Rejected Because

hasil kurang konsisten.

Consequences

* transparansi

− waktu inferensi meningkat

---

# ADR-006

Title

No Persistence

Date

2026-06-21

Status

ACCEPTED

Decision

Tidak menyimpan data klinis.

Context

Privasi dan penyederhanaan sistem.

Alternatives

Prediction History

Rejected Because

menambah risiko privasi.

Consequences

* lebih aman

− tidak ada histori

---

# ADR-007

Title

Stateless API

Date

2026-06-21

Status

ACCEPTED

Decision

Setiap request berdiri sendiri.

Context

Sesuai arsitektur backend.

Alternatives

Session-Based

Rejected Because

menambah kompleksitas.

Consequences

* scalable

− request explain harus kirim ulang data

---

# ADR-008

Title

Prediction Communication

Date

2026-06-21

Status

ACCEPTED

Decision

Layer hasil dipisah menjadi:

Ringkasan

↓

Detail

Context

User awam mudah panik.

Alternatives

Tampilkan probability langsung

Rejected Because

berpotensi disalahartikan.

Consequences

* lebih ramah

− pengguna teknis perlu klik tambahan

---

# ADR-009

Title

Probability Visibility

Date

2026-06-21

Status

ACCEPTED

Decision

Persentase tidak ditampilkan di layar utama.

Context

Mencegah interpretasi sebagai diagnosis.

Alternatives

Tampilkan skor penuh.

Rejected Because

meningkatkan kecemasan.

Consequences

* komunikasi risiko lebih aman

---

# ADR-010

Title

Multi Step Assessment

Date

2026-06-21

Status

ACCEPTED

Decision

Form dibagi menjadi 3 langkah.

Context

Mengurangi beban kognitif.

Alternatives

Single Long Form

Rejected Because

completion rate rendah.

Consequences

* lebih nyaman

− perlu state management

---

# ADR-011

Title

Frontend State Strategy

Date

2026-06-21

Status

ACCEPTED

Decision

Menggunakan Alpine.js state.

Context

Form multi-step memerlukan penyimpanan sementara.

Alternatives

Vue

React

Rejected Because

lebih kompleks.

Consequences

* ringan

− state global terbatas

---

# ADR-012

Title

Feature Selection Policy

Date

2026-06-21

Status

ACCEPTED

Decision

Menghapus:

year

location

clinical_notes

race:*

Context

Mengurangi noise.

Alternatives

gunakan seluruh fitur

Rejected Because

meningkatkan bias.

Consequences

* lebih sederhana

---

# ADR-013

Title

Train/Test Isolation

Date

2026-06-21

Status

ACCEPTED

Decision

Split dilakukan sebelum preprocessing statistik.

Context

Mencegah data leakage.

Alternatives

clean sebelum split

Rejected Because

evaluasi menjadi bias.

Consequences

* evaluasi valid

---

# ADR-014

Title

Encoding Contract

Date

2026-06-21

Status

ACCEPTED

Decision

gender

Label Encoding

smoking_history

OneHotEncoding

Context

Konsisten dengan kontrak data.

Consequences

* inference konsisten

---

# ADR-015

Title

Output Language

Date

2026-06-21

Status

ACCEPTED

Decision

Output utama menggunakan bahasa non-teknis.

Context

Target utama pengguna awam.

Alternatives

raw ML metrics

Rejected Because

membingungkan.

Consequences

* lebih mudah dipahami

---

# ADR-016

Title

Risk Categorization

Date

2026-06-21

Status

ACCEPTED

Decision

LOW

MEDIUM

HIGH

Context

Komunikasi risiko lebih sederhana.

Alternatives

angka probabilitas

Rejected Because

rawan salah interpretasi.

Consequences

* lebih jelas

---

# ADR-017

Title

Artifact Versioning

Date

2026-06-21

Status

ACCEPTED

Decision

Seluruh artifact wajib versioned.

Artifacts

model.pkl

encoder.pkl

preprocessor.pkl

explainer.pkl

metadata.json

metrics.json

Context

Menjamin reproducibility.

Consequences

* rollback mudah

---

# ADR-018

Title

Documentation Governance

Date

2026-06-21

Status

ACCEPTED

Decision

Perubahan sistem wajib memperbarui dokumen terkait.

Rule

Architecture
→ system_spec

Data
→ data_contract

API
→ api_contract

ML
→ ml_pipeline

UI
→ uiux_spec

Context

Dokumentasi harus selalu sinkron.

Consequences

* tidak terjadi kontradiksi
