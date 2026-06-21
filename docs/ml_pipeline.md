# ML Pipeline Specification

Project: Diabetes Early Risk Prediction Platform
Version: 1.1

Purpose:
Mendefinisikan pipeline Machine Learning resmi untuk training, evaluasi, explainability, artifact management, dan inference.

Consumer:

* ML Engineer
* Backend Service
* MLOps
* Explainability Engine

Source of Truth:

* docs/system_spec.md
* docs/data_contract.md
* docs/api_contract.md

---

# 1. Objective

Membangun model prediksi risiko diabetes yang:

* memiliki recall tinggi,
* stabil terhadap data baru,
* dapat dijelaskan,
* dapat direproduksi.

Prediction Type:

Binary Classification

Target:

diabetes

Mapping:

0 → Negative

1 → Positive

---

# 2. Pipeline Overview

Raw Dataset

↓

Validation

↓

Feature Selection

↓

Train/Test Split

↓

Train-aware Preprocessing

↓

Feature Encoding

↓

SMOTE

↓

Model Training

↓

Evaluation

↓

Explainability

↓

Artifact Export

↓

Inference Deployment

---

# 3. Dataset Rules

Input:

Clinical Structured Dataset

Allowed Features:

* age
* gender
* bmi
* hba1c_level
* blood_glucose_level
* hypertension
* heart_disease
* smoking_history

Forbidden Features:

* year
* location
* clinical_notes
* race:*

Rule:

drop sebelum split.

---

# 4. Train/Test Split

Method:

train_test_split

Config:

test_size = 0.20

stratify = y

random_state = 42

Output:

X_train

X_test

y_train

y_test

Rule:

test set tidak boleh disentuh selama training.

---

# 5. Train-aware Preprocessing

Semua preprocessing statistik wajib menggunakan TRAIN SET sebagai sumber perhitungan.

Transformasi hasil fit diterapkan ke:

* X_train
* X_test
* inference

---

## Missing Values

Numeric:

median

Categorical:

mode

Rule:

fit:

X_train

transform:

X_train
X_test
inference

---

## Duplicate Handling

remove exact duplicate

Rule:

training only

---

## Outlier Handling

Method:

IQR clipping

Formula:

Lower:

Q1 − 1.5×IQR

Upper:

Q3 + 1.5×IQR

Rule:

fit:

X_train

transform:

X_train
X_test
inference

---

# 6. Feature Engineering

Rule:

Training dan inference wajib menggunakan transformasi identik.

Semua encoder wajib disimpan.

---

## Encoding

Method 1

Label Encoding

Columns:

gender

Mapping:

Male → 0

Female → 1

---

Method 2

OneHotEncoding

Columns:

smoking_history

Categories:

* never
* former
* current
* not_current
* unknown

Rule:

export:

encoder.pkl

---

## Numerical Features

No scaling.

Reason:

Random Forest tidak membutuhkan normalisasi.

---

# 7. Imbalanced Handling

Problem:

kelas minoritas rendah.

Method:

SMOTE

Library:

imbalanced-learn

Config:

sampling_strategy = 0.5

random_state = 42

Flow

X_train

↓

SMOTE

↓

X_train_balanced

Rules:

SMOTE hanya pada train.

Forbidden:

❌ sebelum split

❌ pada test

❌ pada inference

---

Expected Ratio

Before:

91.5 / 8.5

After:

50 / 50

---

# 8. Model Training

Algorithm:

RandomForestClassifier

Baseline Config

n_estimators = 300

max_depth = 10

min_samples_split = 10

min_samples_leaf = 4

class_weight = balanced

random_state = 42

n_jobs = -1

Rule:

gunakan konfigurasi tetap.

---

# 9. Hyperparameter Tuning

Method:

RandomizedSearchCV

CV:

5 Fold

Scoring:

recall

Search Budget:

≤ 100

Rule:

train only.

Output:

best_model

---

# 10. Evaluation

Primary Metric

Recall

Target:

≥ 0.85

---

Secondary

F1 Score

ROC-AUC

Precision

Specificity

---

Diagnostic Metrics

Confusion Matrix

False Negative Rate

False Positive Rate

---

Acceptance Criteria

Recall:

≥ 0.85

FNR:

≤ 0.15

ROC-AUC:

≥ 0.80

---

# 11. Model Selection

Priority

1 Recall

2 ROC-AUC

3 F1

4 Precision

Tie Breaker:

pilih model lebih sederhana.

---

# 12. Threshold Strategy

Default Threshold

0.50

Risk Mapping

0.00–0.29

LOW

0.30–0.69

MEDIUM

0.70–1.00

HIGH

Rule:

threshold dikonfigurasi pada deployment.

---

# 13. Explainability

Method:

SHAP

Engine:

TreeExplainer

Inputs:

trained_model

X_sample

Outputs:

global_importance

local_importance

summary_plot

waterfall_plot

---

Frontend Output

max:

5 faktor

Example

↑ Blood Glucose

impact:

34

description:

"Memberi pengaruh besar terhadap peningkatan risiko."

Rules:

❌ jangan tampilkan SHAP mentah

❌ jangan tampilkan nilai tanpa konteks

Gunakan:

✅ narasi manusia

---

# 14. Artifact Management

Output Directory

/models

Artifacts

model.pkl

encoder.pkl

preprocessor.pkl

explainer.pkl

metadata.json

metrics.json

---

metadata.json

{

"version":"1.1",

"algorithm":"RandomForest",

"recall":0.88,

"threshold":0.50

}

Rules:

semua artifact versioned.

---

# 15. Inference Pipeline

Request

↓

Validate

↓

Load Preprocessor

↓

Transform

↓

Predict

↓

Probability

↓

SHAP

↓

Format Response

Rule:

transformasi inference harus identik dengan training.

---

Latency

< 1 sec

Batch

unsupported

---

# 16. Monitoring

Track

prediction_count

latency

confidence

feature_distribution

model_drift

---

Drift Trigger

feature drift > 20%

confidence drop > 10%

recall drop > 5%

Action

manual retraining

---

# 17. Retraining Policy

Phase 1

manual

Future

automatic

Trigger

* dataset baru
* drift
* performa turun

---

# 18. Reproducibility

Seed

42

Environment

Python 3.12

Libraries

pandas

numpy

scikit-learn

imbalanced-learn

shap

joblib

Rule:

training ulang harus menghasilkan performa serupa.

---

# 19. Ownership

ML:

training

Backend:

serving

Frontend:

visualization

Perubahan pipeline wajib update:

* ml_pipeline.md
* api_contract.md
* metadata.json
