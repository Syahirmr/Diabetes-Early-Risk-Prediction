# System Specification

Project: Diabetes Early Risk Prediction Platform
Version: 1.0
Architecture: Decoupled Architecture (Frontend + Backend API + Machine Learning Service)

---

# 1. Project Overview

## Purpose

Membangun platform prediksi risiko Diabetes Mellitus berbasis Machine Learning yang membantu masyarakat umum memahami kondisi kesehatannya melalui pengalaman yang edukatif, transparan, dan mudah dipahami.

Sistem berfungsi sebagai alat deteksi dini berbasis data klinis dan bukan alat diagnosis medis.

---

## Vision

Menyediakan pemeriksaan risiko diabetes yang:

* mudah digunakan,
* dapat dijelaskan,
* berbasis data,
* mendukung deteksi dini,
* meningkatkan kesadaran kesehatan masyarakat.

---

## Product Positioning

Produk ini merupakan:

Health Education Platform
+
Risk Prediction System
+
Explainable AI Experience

Bukan:

* aplikasi diagnosis,
* sistem rekam medis,
* alat konsultasi dokter.

---

# 2. Goals & Non-Goals

## Goals

Sistem harus mampu:

1. Mengedukasi pengguna mengenai diabetes.
2. Mengumpulkan parameter klinis secara interaktif.
3. Menghasilkan prediksi risiko berbasis Machine Learning.
4. Menjelaskan faktor yang memengaruhi hasil prediksi.
5. Memberikan rekomendasi tindakan lanjutan yang aman.

---

## Non-Goals

Sistem tidak boleh:

* menyatakan diagnosis medis,
* memberi resep obat,
* menggantikan tenaga kesehatan,
* menyimpan identitas pribadi,
* membuat keputusan klinis otomatis.

---

# 3. Target Users

## Primary Users

Masyarakat umum:

* usia 20–60 tahun,
* tidak memiliki latar belakang medis,
* ingin melakukan pemeriksaan mandiri.

---

## Secondary Users

* mahasiswa,
* peneliti,
* tenaga kesehatan untuk edukasi.

---

# 4. Product Principles

## Education First

Sebelum melakukan prediksi, pengguna harus memahami konteks kesehatan.

---

## Explain Before Predict

Setiap input dan hasil harus dapat dijelaskan.

---

## Human-Friendly + Transparent

Output harus mudah dipahami tetapi tetap transparan secara teknis.

---

## Privacy First

Tidak menyimpan identitas pengguna.

---

## Safety-Oriented

Menghindari bahasa yang dapat dianggap sebagai diagnosis.

---

# 5. High-Level Architecture

Frontend
(UI + Education Layer)

↓

REST API

↓

Prediction Service

↓

Machine Learning Pipeline

↓

Explainability Engine

↓

Response Formatter

↓

Frontend Result View

---

# 6. Functional Requirements

## FR-001 Landing & Education

Sistem menyediakan halaman edukasi yang menjelaskan:

* apa itu diabetes,
* urgensi diabetes,
* prevalensi global,
* prevalensi Indonesia,
* faktor risiko,
* pentingnya deteksi dini.

Output:
Landing page edukatif.

---

## FR-002 Clinical Assessment

Sistem menyediakan form input interaktif.

Input:

Demografi:

* age
* gender

Klinis:

* bmi
* hba1c_level
* blood_glucose_level
* hypertension
* heart_disease
* smoking_history

Requirement:

* validasi real-time,
* bantuan penjelasan,
* contoh nilai input.

---

## FR-003 Prediction

Frontend mengirim data ke API.

Backend melakukan:

* preprocessing,
* inferensi,
* evaluasi risiko,
* penjelasan hasil.

Output:

* risk level
* probability
* confidence
* explanation

---

## FR-004 Explainability

Sistem wajib menjelaskan:

* faktor yang meningkatkan risiko,
* faktor yang menurunkan risiko,
* kontribusi tiap fitur.

Explainability menggunakan:

SHAP

Output:

* visual sederhana,
* narasi manusia.

---

## FR-005 Recommendation

Sistem memberikan:

* edukasi,
* tindakan lanjutan,
* saran pemeriksaan.

---

# 7. User Experience Requirements

User Flow:

Landing

↓

Education

↓

Assessment

↓

Prediction

↓

Interpretation

↓

Recommendation

Rules:

* maksimal 3 langkah input,
* mobile-first,
* gunakan bahasa sederhana.

---

# 8. Prediction Result Rules

Output menggunakan dua layer.

---

## Layer 1 — Ringkasan (Default)

Ditampilkan untuk semua pengguna.

Contoh:

━━━━━━━━━━━━━━━

HASIL PEMERIKSAAN

🟠 Risiko Diabetes: Tinggi

Interpretasi:

"Berdasarkan data yang dimasukkan, terdapat indikasi risiko diabetes yang perlu diperhatikan."

━━━━━━━━━━━━━━━

---

## Layer 2 — Detail Analisis

Ditampilkan jika user membuka detail.

Menampilkan:

Skor Risiko:
87%

Confidence:
0.87

Kontributor:

↑ Blood Glucose

↑ HbA1c

↑ BMI

Model:

Random Forest

Explainability:

SHAP

---

Rules:

Jangan tampilkan:

❌ Probability tanpa konteks

❌ SHAP mentah

❌ Feature importance mentah

Gunakan:

✅ Skor + interpretasi

✅ Faktor dominan

✅ Bahasa sederhana

---

Disclaimer:

"Hasil ini bukan diagnosis medis."

---

# 9. Machine Learning Requirements

Objective:

Memaksimalkan deteksi risiko.

Target:

Recall tinggi.

Pipeline:

Split

↓

SMOTE

↓

Random Forest

↓

Evaluation

↓

SHAP

Rules:

* SMOTE hanya pada train
* inference deterministik
* reproducible

Primary Metric:

Recall

Secondary:

* F1 Score
* ROC-AUC
* Precision

Target:

Recall ≥ 0.85

---

# 10. Data Principles

Target:

diabetes

Mapping:

0 → Negative

1 → Positive

Drop:

* year
* location
* clinical_notes
* race:*

Forbidden:

* nama
* email
* alamat
* nomor identitas

Storage:

anonymous only

---

# 11. Non-Functional Requirements

Response:

≤ 3 detik

Availability:

99%

Browser:

* Chrome
* Edge
* Safari

Accessibility:

WCAG AA

Deployment:

stateless

Security:

HTTPS only

---

# 12. Risk Communication Rules

LOW

"Pertahankan pola hidup sehat."

---

MEDIUM

"Pertimbangkan pemeriksaan lanjutan."

---

HIGH

"Konsultasikan dengan tenaga medis."

---

Dilarang:

❌ Positif Diabetes

❌ Anda terkena diabetes

Gunakan:

✅ Risiko meningkat

✅ Indikasi perlu diperiksa

---

# 13. Success Metrics

Technical:

Recall:
≥ 0.85

Latency:
≤ 3 sec

Error:
< 2%

---

Product:

Form Completion:
≥ 80%

Prediction Success:
≥ 95%

Bounce:
< 40%

---

# 14. Out of Scope

Tidak termasuk:

* autentikasi
* pembayaran
* rekam medis
* integrasi rumah sakit
* telemedicine
* chatbot medis

---

# 15. Future Roadmap

Phase 1

Prediction + Explainability

Phase 2

Dashboard

Phase 3

Monitoring

Phase 4

Continuous Learning

Phase 5

Clinical Integration

---

# 16. Ownership Rules

Frontend:
UX

Backend:
API

ML:
Model

Perubahan lintas modul wajib melalui revisi spesifikasi.
