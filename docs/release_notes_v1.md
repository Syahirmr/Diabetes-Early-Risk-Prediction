# Release Notes v1.0 - Diabetes Early Risk Prediction Platform

## Pencapaian & Arsitektur Utama

Sepanjang siklus pengembangan (Phase 1 hingga Phase 7), sistem ini telah berevolusi dari sebatas prototipe Machine Learning menjadi produk siap pakai berstandar industri dengan fokus kuat pada keandalan dan pengalaman pengguna. Berikut adalah fitur arsitektur unggulan dari rilis v1.0 ini:

1. **Decoupled FastAPI & Alpine.js**
   Arsitektur Frontend dan Backend terpisah sepenuhnya (*decoupled*). Hal ini memfasilitasi skalabilitas yang lebih baik, kemudahan pengujian independen (End-to-End dengan Playwright maupun HTTP Client), serta lokalisasi *error* tanpa mempengaruhi lapisan lainnya.

2. **Memory-Resident ML Artifacts**
   Model *Random Forest*, objek *Scaler/Encoder*, serta abstraksi komputasi berat *SHAP TreeExplainer* diinisialisasi secara efisien menggunakan pola *Singleton Scope* pada memori saat proses *startup* API (via `lifespan`). Teknik ini secara revolusioner mempertahankan metrik inferensi dan total *latency* di bawah batasan 2-3 detik (berdasarkan *Stress Test*) sekalipun melayani 50 *concurrent requests*.

3. **Fail-Fast & Fallback Mechanism (UX Resilience)**
   Aplikasi dilindungi oleh batas Pydantic yang absolut (*Edge Cases Constraint*) di lapis pelindung Backend sehingga payload "sampah" akan diblokir dengan kode 422 sebelum sempat merusak memori. Di sisi *Frontend*, Alpine.js menerapkan pola adaptasi *Graceful Degradation* yang secara natural menangani anomali teknis menjadi bahasa Indonesia yang sopan dan ramah—memastikan pengguna tidak pernah mengalami fenomena layar kosong (*UI Blanking/Dead End*).

## Panduan Eksekusi (Dosen Penguji / Reviewer)
Sistem ini telah dilengkapi dengan kontainerisasi *Docker Compose*. Untuk menjalankan integrasi penuh secara instan tanpa perlu menyetel *environment* satu-per-satu, cukup jalankan perintah:

```bash
docker-compose up --build
```
- **Frontend** akan tersedia di: `http://localhost:3000`
- **Backend API & Swagger Docs** akan tersedia di: `http://localhost:8000/docs`

> **Note:** Sesuai kebijakan kepatuhan keamanan data aplikasi, pastikan Anda telah meletakkan *folder* `/models` di direktori *root* sebelum melakukan *build*, dikarenakan berkas berukuran raksasa (`.pkl`) tidak disertakan di dalam struktur mentah *Docker image* untuk mempercepat proses transmisi data.
