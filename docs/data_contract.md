# Data Contract

Project: Diabetes Early Risk Prediction Platform
Version: 1.0

Purpose:
Dokumen ini mendefinisikan struktur data resmi yang digunakan oleh seluruh komponen sistem.

Consumer:

* Frontend
* Backend API
* Machine Learning Pipeline
* Explainability Engine

Source of Truth:
docs/system_spec.md

---

# 1. General Rules

Semua data harus:

* tervalidasi,
* konsisten,
* deterministic,
* backward compatible.

Tidak boleh ada transformasi diam-diam di frontend.

Semua preprocessing dilakukan di backend.

---

# 2. Dataset Definition

Dataset Type:
Clinical Structured Dataset

Prediction Type:
Binary Classification

Target:

diabetes

Mapping:

0 → Negative

1 → Positive

---

# 3. Allowed Features

## Demographic Features

| Field  | Type    | Required |
| ------ | ------- | -------- |
| age    | integer | YES      |
| gender | string  | YES      |

Allowed:

gender:

* Male
* Female

---

## Clinical Features

| Field               | Type    | Required |
| ------------------- | ------- | -------- |
| bmi                 | float   | YES      |
| hba1c_level         | float   | YES      |
| blood_glucose_level | integer | YES      |
| hypertension        | integer | YES      |
| heart_disease       | integer | YES      |
| smoking_history     | string  | YES      |

Allowed:

hypertension:
0
1

heart_disease:
0
1

smoking_history:

* never
* former
* current
* not_current
* unknown

---

# 4. Removed Features

Kolom berikut tidak boleh masuk model.

| Feature        |
| -------------- |
| year           |
| location       |
| clinical_notes |
| race:*         |

Rule:

drop sebelum training.

drop sebelum inference.

Reason:

* mengurangi noise,
* menghindari bias,
* tidak relevan secara klinis.

---

# 5. Validation Rules

## age

Type:
integer

Range:

18–120

Examples:

VALID:
45

INVALID:
-10

---

## bmi

Type:
float

Range:

10–80

Unit:

kg/m²

Example:

VALID:
28.4

---

## hba1c_level

Type:
float

Range:

3–20

Unit:

%

Example:

VALID:
6.5

---

## blood_glucose_level

Type:
integer

Range:

40–500

Unit:

mg/dL

Example:

VALID:
145

---

## hypertension

Allowed:

0
1

---

## heart_disease

Allowed:

0
1

---

## smoking_history

Allowed:

never
former
current
not_current
unknown

---

# 6. Missing Value Policy

Training:

Numeric:
median

Categorical:
mode

Inference:

missing value
→ reject request

HTTP:
422

---

# 7. Duplicate Handling

Training:

remove exact duplicate

Inference:

not applicable

---

# 8. Outlier Policy

Training:

IQR clipping

Rule:

Q1 − 1.5×IQR

Q3 + 1.5×IQR

Inference:

gunakan validasi range.

---

9. Encoding Rules
gender:
Label Encoding (Male → 0, Female → 1)

hypertension & heart_disease:
Pass-through (Frontend langsung mengirim integer 0 atau 1)

smoking_history:
OneHotEncoding
Rule:
1. Encoding HANYA dilakukan di backend. Frontend mengirim nilai string asli ("never", "former", dll).
2. Backend WAJIB menyimpan objek `encoder` (misal: `encoder.pkl`) atau melakukan *column alignment* saat *inference* untuk memastikan jumlah fitur tidak *mismatch* dengan model.

---

# 10. Train/Test Contract

Split:

80 / 20

Method:

stratified

Random Seed:

42

Rule:

SMOTE hanya pada train.

Jangan pernah melakukan resampling pada test.

---

# 11. Request Payload Contract

Frontend → Backend

Content-Type:

application/json

Example:

{
"age":45,
"gender":"Male",
"bmi":31.2,
"hba1c_level":7.0,
"blood_glucose_level":190,
"hypertension":1,
"heart_disease":0,
"smoking_history":"former"
}

---

# 12. Internal Model Input

Contoh:

[
45,
0,
31.2,
7.0,
190,
1,
0,
0,
1,
0,
0
]

Rule:

frontend tidak pernah melihat format ini.

---

# 13. Prediction Response Contract

Backend → Frontend

Example:

{
"risk_level":"High",
"risk_score":87,
"confidence":0.87,
"prediction":1,
"top_factors":[
{
"feature":"blood_glucose_level",
"direction":"increase",
"impact":34
},
{
"feature":"hba1c_level",
"direction":"increase",
"impact":26
}
],
"message":"Terdapat indikasi risiko diabetes yang perlu diperhatikan."
}

---

# 14. Explainability Contract

Engine:

SHAP

Top Features:

max 5

Output Rules:

Raw:

0.423

Frontend:

"Memberi pengaruh tinggi"

---

Direction:

positive
negative

Mapped:

increase
decrease

---

# 15. Error Contract

Validation Error

422

Example:

{
"code":"INVALID_INPUT",
"message":"BMI harus berada pada rentang 10–80"
}

---

Missing Field

400

Example:

{
"code":"MISSING_FIELD"
}

---

Prediction Error

500

Example:

{
"code":"PREDICTION_FAILED"
}

---

# 16. Privacy Rules

Jangan simpan:

* nama
* email
* alamat
* nomor identitas

Logging:

anonymous only

Retention:

0 hari

No database persistence.

---

# 17. Versioning

Current:

v1

Breaking change:

major version

Backward compatible:

minor version

Example:

v1.0
v1.1
v2.0
