# UI/UX Specification

Project: Diabetes Early Risk Prediction Platform
Version: 1.1

Purpose:
Mendefinisikan standar pengalaman pengguna agar sistem prediksi diabetes mudah dipahami, edukatif, transparan, dan aman digunakan oleh masyarakat umum.

Consumer:

* Frontend Engineer
* UI Designer
* UX Designer
* Product Designer

Source of Truth:

* docs/system_spec.md
* docs/data_contract.md
* docs/api_contract.md

---

# 1. Design Philosophy

Produk ini bukan dashboard medis.

Produk ini adalah:

Health Education Platform

*

Risk Prediction Experience

*

Explainable AI Interface

---

Experience Goal

"User memahami kondisi kesehatannya dengan lebih baik setelah menggunakan sistem."

---

Flow Philosophy

Educate

↓

Assess

↓

Predict

↓

Explain

↓

Recommend

---

# 2. Target Persona

Primary User

Usia:
20–60

Background:
non-medis

Karakteristik:

* ingin cepat memahami hasil,
* tidak familiar dengan istilah medis,
* dominan menggunakan smartphone.

---

Secondary User

* mahasiswa
* peneliti
* tenaga kesehatan

---

# 3. Design Principles

## P1 Progressive Disclosure

Informasi sederhana ditampilkan terlebih dahulu.

Detail teknis dibuka jika diinginkan.

---

## P2 Human-Friendly

Bahasa mudah dipahami.

---

## P3 Transparent AI

Model boleh dijelaskan.

Hasil tidak boleh menyesatkan.

---

## P4 Non-Diagnostic

Sistem tidak melakukan diagnosis.

---

## P5 Accessibility First

Semua pengguna dapat menggunakan sistem tanpa hambatan.

---

# 4. User Journey

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

↓

(Optional)

Download Result

---

# 5. Page Structure

## Page 1 — Landing

Goal

Membangun awareness.

Sections

Hero

↓

Urgency

↓

Risk Factors

↓

How It Works

↓

CTA

---

Hero

Title

Cek Risiko Diabetes Lebih Awal

Subtitle

Gunakan data kesehatan sederhana untuk memahami faktor risiko diabetes.

CTA

Mulai Pemeriksaan

---

Urgency

Tampilkan:

* prevalensi global
* prevalensi Indonesia
* pentingnya deteksi dini

Visual

cards

---

Risk Factors

Cards

* gula darah
* HbA1c
* BMI
* hipertensi
* riwayat jantung

---

How It Works

1 Input Data

↓

2 Analisis

↓

3 Interpretasi

---

Footer

Disclaimer

Bukan alat diagnosis medis.

---

# 6. Assessment Experience

Goal

Mengumpulkan data secara nyaman.

Rules

* maksimal 3 langkah
* WAJIB progress indicator
* WAJIB tombol Next
* WAJIB tombol Back
* data harus tetap tersimpan saat pindah langkah

State Management

Temporary State

Framework:

Alpine.js

Rules

* data tidak hilang saat kembali
* submit hanya di langkah terakhir

---

Step 1

Profil Dasar

Fields

* age
* gender

---

Step 2

Riwayat Kesehatan

Fields

* hypertension
* heart_disease
* smoking_history

---

Step 3

Parameter Klinis

Fields

* bmi
* hba1c_level
* blood_glucose_level

---

Progress UI

Step 1

● ○ ○

Step 2

● ● ○

Step 3

● ● ●

---

# 7. Input Components

Setiap field wajib memiliki:

Label

Tooltip

Placeholder

Validation

Helper Text

---

Example

HbA1c

Helper

Menggambarkan rata-rata gula darah beberapa bulan terakhir.

Placeholder

6.5

---

Blood Glucose

Helper

Hasil pemeriksaan gula darah.

Placeholder

140

---

BMI

Helper

Perbandingan berat dan tinggi badan.

Placeholder

28.5

---

Validation

Jangan:

Invalid Input

Gunakan:

Masukkan nilai antara 40–500

---

# 8. Loading Experience

Goal

Mengurangi kecemasan pengguna.

Saat prediksi:

Tampilkan:

Loading State

Message

Sedang menganalisis data...

Subtext

Kami sedang menghitung faktor risiko Anda.

Animation

subtle

Max Duration

3 detik

---

# 9. Result Experience

Output menggunakan 2 layer.

---

Layer 1

Ringkasan (Default)

Goal

Menghindari kepanikan.

Fokus pada kategori.

Tampilkan

Visual Gauge

Risk Badge

Summary

Recommendation

---

Contoh

━━━━━━━━━━━━━━

HASIL PEMERIKSAAN

🟠 Risiko Diabetes

TINGGI

(Gauge berada di area oranye)

Interpretasi

Terdapat indikasi risiko yang perlu diperhatikan.

Rekomendasi

Pertimbangkan pemeriksaan lanjutan.

━━━━━━━━━━━━━━

Rules

Jangan tampilkan:

❌ angka probabilitas

❌ confidence

❌ probability

---

Layer 2

Detail Analisis

Expandable.

Goal

Transparansi.

Tampilkan

Skor Risiko

Confidence

Model

Faktor Dominan

Explainability

---

Contoh

Skor Risiko

87%

Confidence

0.87

Model

Random Forest

Faktor

↑ Glukosa

↑ HbA1c

↑ BMI

---

Rules

Gunakan:

skor + interpretasi

Jangan:

SHAP mentah

Feature Importance mentah

---

Disclaimer

Hasil ini bukan diagnosis medis.

---

# 10. Explainability Experience

Goal

User memahami alasan hasil.

Visual

Top Contributors

Maximum

5

Format

↑ meningkatkan risiko

↓

menurunkan risiko

---

Contoh

↑ Kadar gula tinggi

↓

BMI normal

---

Narasi

Gunakan:

"Kadar gula memiliki pengaruh besar terhadap hasil."

Jangan:

"SHAP = 0.42"

---

# 11. Recommendation Experience

LOW

Pertahankan pola hidup sehat.

---

MEDIUM

Pertimbangkan pemeriksaan lanjutan.

---

HIGH

Konsultasikan dengan tenaga medis.

---

Rules

Actionable

Bukan diagnosis

---

# 12. Error Experience

Validation

Masukkan data yang valid.

---

API

Kami belum bisa memproses sekarang.

---

Network

Periksa koneksi Anda.

---

Empty

Ayo mulai pemeriksaan.

---

# 13. Accessibility

Contrast

WCAG AA

Font

≥16px

Tap Area

≥44px

Keyboard

supported

Mobile

required

---

# 14. Responsive Rules

Desktop

max-width:
1280

---

Tablet

2 column

---

Mobile

single column

sticky CTA

---

# 15. Visual System

Primary

Blue

trust

---

Accent

Green

health

---

Warning

Orange

attention

---

High Risk

Red

awareness

---

Rule

hindari warna ekstrem.

---

# 16. Copywriting Rules

Gunakan

risiko

indikasi

pemeriksaan

pemahaman

---

Jangan gunakan

positif diabetes

terkena diabetes

diagnosis

penyakit pasti

---

# 17. Download Result

Optional

Format

PDF

Isi

* ringkasan
* faktor dominan
* disclaimer

Jangan sertakan:

* confidence
* probability mentah
* output teknis

---

# 18. Ownership

Frontend

implement

UX

validate

Backend

provide data

Perubahan wajib update:

* uiux_spec.md
* api_contract.md
