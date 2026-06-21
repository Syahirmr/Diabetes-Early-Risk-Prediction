# API Contract

Project: Diabetes Early Risk Prediction Platform
Version: 1.1

Purpose:
Mendefinisikan kontrak komunikasi resmi antara Frontend ↔ Backend API.

Source of Truth:

* docs/system_spec.md
* docs/data_contract.md

Architecture:
Decoupled + Stateless

---

# 1. API Principles

API harus:

* stateless,
* deterministic,
* reproducible,
* versioned,
* backward compatible.

Rules:

* seluruh komunikasi menggunakan JSON,
* frontend tidak melakukan preprocessing,
* backend melakukan validasi,
* backend melakukan encoding,
* backend melakukan inferensi,
* backend menghasilkan explainability.

Tidak boleh ada penyimpanan state antar request.

---

# 2. Base Configuration

Protocol:

HTTPS

Base URL:

/api/v1

Content-Type:

application/json

Encoding:

UTF-8

Timeout:

3 sec

---

# 3. Endpoint Overview

| Method | Endpoint  | Description                 |
| ------ | --------- | --------------------------- |
| GET    | /health   | Health Check                |
| GET    | /metadata | Model Metadata              |
| POST   | /predict  | Prediction + Explainability |
| POST   | /explain  | Extended Explainability     |

---

# 4. GET /health

Purpose:

Memastikan service aktif.

Request:

None

Response:

200

{
"status":"healthy",
"service":"prediction-api",
"version":"1.1"
}

---

# 5. GET /metadata

Purpose:

Mengambil metadata model aktif.

Response:

200

{
"model":"RandomForest",
"version":"1.0",
"target":"diabetes",
"metric":"recall",
"explainability":"SHAP"
}

Rules:

Tidak mengembalikan parameter internal model.

---

# 6. POST /predict

Purpose:

Melakukan prediksi risiko diabetes dan menghasilkan interpretasi.

Request:

{
"age":45,
"gender":"Male",
"bmi":31.2,
"hba1c_level":7.0,
"blood_glucose_level":180,
"hypertension":1,
"heart_disease":0,
"smoking_history":"former"
}

Validation:

* seluruh field wajib
* mengikuti docs/data_contract.md

---

Processing Flow

Validate

↓

Preprocess

↓

Encode

↓

Predict

↓

SHAP

↓

Format Response

---

Response

200

{
"success":true,

"prediction":{

"risk_level":"High",

"risk_score":87,

"confidence":0.87,

"prediction_code":1

},

"summary":{

"title":"Risiko Diabetes Tinggi",

"message":"Berdasarkan data yang dimasukkan, terdapat indikasi risiko yang perlu diperhatikan."

},

"explanation":{

"top_factors":[

{
"feature":"blood_glucose_level",

"display":"Kadar Gula Darah",

"direction":"increase",

"impact":34,

"description":"Memberi pengaruh cukup besar terhadap peningkatan risiko."
},

{
"feature":"hba1c_level",

"display":"HbA1c",

"direction":"increase",

"impact":26,

"description":"Nilai lebih tinggi dari rentang umum."
}

]

},

"recommendation":[

"Pertimbangkan pemeriksaan lanjutan",

"Konsultasikan dengan tenaga medis"

],

"disclaimer":

"Hasil ini bukan diagnosis medis."

}

---

Field Rules

risk_level:

LOW
MEDIUM
HIGH

risk_score:

0–100

confidence:

0–1

prediction_code:

0
1

top_factors:

max 5

---

# 7. POST /explain

Purpose:

Menghasilkan penjelasan lebih rinci.

Karena sistem bersifat STATELESS,
endpoint ini wajib menerima ulang payload klinis lengkap.

Request:

{
"age":45,
"gender":"Male",
"bmi":31.2,
"hba1c_level":7.0,
"blood_glucose_level":180,
"hypertension":1,
"heart_disease":0,
"smoking_history":"former"
}

Processing

Validate

↓

Preprocess

↓

Predict

↓

Generate SHAP

↓

Return Explanation

---

Response

200

{
"success":true,

"model":"RandomForest",

"method":"SHAP",

"top_positive":[

{
"feature":"blood_glucose",

"impact":42,

"description":"Memberi kontribusi besar terhadap peningkatan risiko."
}

],

"top_negative":[

{
"feature":"bmi",

"impact":-13,

"description":"Memberi kontribusi menurunkan risiko."
}

]

}

Rules:

Tidak menggunakan:

prediction_id

Tidak menyimpan hasil sebelumnya.

---

# 8. Error Contract

Format:

{
"success":false,

"error":{

"code":"",

"message":"",

"details":[]
}

}

---

400

INVALID_REQUEST

---

422

VALIDATION_ERROR

---

429

TOO_MANY_REQUESTS

---

500

PREDICTION_FAILED

Example:

{
"success":false,

"error":{

"code":"VALIDATION_ERROR",

"message":"BMI harus berada pada rentang 10–80"
}

}

---

# 9. Security Rules

Headers:

Accept:
application/json

Content-Type:
application/json

---

CORS Policy

Backend WAJIB mengizinkan origin frontend yang telah dikonfigurasi.

Development:

http://localhost:3000

Production:

environment variable

Rules:

* jangan gunakan wildcard (*)
* hanya origin terdaftar
* preflight OPTIONS wajib didukung

Example:

Access-Control-Allow-Origin

Access-Control-Allow-Headers

Access-Control-Allow-Methods

---

Authentication

Tidak digunakan.

---

Session

Tidak digunakan.

---

Cookie

Tidak digunakan.

---

Transport

HTTPS only

---

Forbidden

* HTML
* XML

---

# 10. Rate Limiting

Anonymous:

30 req/min

Burst:

10 request

Response:

429

---

# 11. Logging Rules

Allowed:

* timestamp
* endpoint
* latency
* status

Forbidden:

* payload klinis
* identitas user
* hasil prediksi

Retention:

7 hari

---

# 12. Versioning Rules

Current:

v1

Pattern:

/api/v1

Breaking:

major

Non-breaking:

minor

Examples:

v1.0

v1.1

v2.0

---

# 13. Ownership Rules

Frontend:

consume API

Backend:

implement API

ML:

return prediction only

Schema change wajib update:

* system_spec.md
* data_contract.md
* api_contract.md
