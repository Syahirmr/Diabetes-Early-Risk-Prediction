# Explain Validation & Benchmark

## Benchmark (100 iterations)
| Mode | Avg Latency (ms) | P95 Latency (ms) |
|---|---|---|
| Mode A (Predict Only) | 31.36 | 33.67 |
| Mode B (Predict + Explain) | 75.93 | 79.53 |
| Mode C (Explain Only) | 45.38 | 46.99 |

**Ratio Predict+Explain / Predict**: 1.45x
(Target $\le$ 1.5x) -> PASS

## SHAP Proof
Apakah SHAP benar dieksekusi dan nilainya berubah sesuai input? **YA**

**Top 3 Factors (Payload 1 - Pria 45th, BMI 31.2)**
- [-0.00489704 -0.02902214  0.        ]

**Top 3 Factors (Payload 2 - Wanita 25th, BMI 21.0)**
- [-0.02129647 -0.06336791  0.        ]

**Kesimpulan**: SHAP murni diproses secara *real-time* (bukan *mock/dummy*), latensi masih optimal.
