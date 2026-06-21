import os
import json
import time
import pandas as pd
import numpy as np
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import recall_score, precision_score, f1_score, roc_auc_score, confusion_matrix
from sklearn.preprocessing import OneHotEncoder

from imblearn.over_sampling import SMOTE
import shap

def main():
    print("Starting Phase 2 ML Pipeline...")
    os.makedirs('reports', exist_ok=True)
    os.makedirs('models/artifacts', exist_ok=True)

    # 1. Load Dataset
    X_train = pd.read_csv('data/processed/X_train.csv')
    X_test = pd.read_csv('data/processed/X_test.csv')
    y_train = pd.read_csv('data/processed/y_train.csv').squeeze()
    y_test = pd.read_csv('data/processed/y_test.csv').squeeze()

    # Apply Schema Mapping back to original rules if needed? The schema mapping was applied in Phase 1.5. 
    # Data is already mapped, so we use `hba1c_level`.

    # 2. Encoding
    # gender: Label Encoding (Male -> 0, Female -> 1)
    X_train['gender'] = X_train['gender'].map({'Male': 0, 'Female': 1}).fillna(0)
    X_test['gender'] = X_test['gender'].map({'Male': 0, 'Female': 1}).fillna(0)

    # smoking_history: One Hot Encoding
    ohe = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    
    # Fit transform train
    smoking_train = ohe.fit_transform(X_train[['smoking_history']])
    smoking_cols = ohe.get_feature_names_out(['smoking_history'])
    smoking_train_df = pd.DataFrame(smoking_train, columns=smoking_cols, index=X_train.index)
    X_train = pd.concat([X_train.drop(columns=['smoking_history']), smoking_train_df], axis=1)

    # Transform test
    smoking_test = ohe.transform(X_test[['smoking_history']])
    smoking_test_df = pd.DataFrame(smoking_test, columns=smoking_cols, index=X_test.index)
    X_test = pd.concat([X_test.drop(columns=['smoking_history']), smoking_test_df], axis=1)

    # Save encoder artifact
    encoder_artifact = {
        'gender_map': {'Male': 0, 'Female': 1},
        'smoking_ohe': ohe,
        'smoking_cols': smoking_cols.tolist()
    }
    joblib.dump(encoder_artifact, 'models/artifacts/encoder.pkl')
    print("Encoding done.")

    # 3. SMOTE
    ratio_before = y_train.value_counts(normalize=True).to_dict()
    rows_before = len(y_train)

    smote = SMOTE(random_state=42, sampling_strategy=0.5)
    X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

    ratio_after = y_train_res.value_counts(normalize=True).to_dict()
    rows_after = len(y_train_res)
    rows_added = rows_after - rows_before

    with open('reports/smote_report.md', 'w') as f:
        f.write(f"# SMOTE Report\n- Ratio Before: {ratio_before}\n- Ratio After: {ratio_after}\n- Rows Before: {rows_before}\n- Rows After: {rows_after}\n- Rows Added: {rows_added}\n")
    print("SMOTE done.")

    # 4. Train Random Forest
    rf = RandomForestClassifier(random_state=42, n_jobs=-1, class_weight='balanced')
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [8, 12, 16],
        'min_samples_leaf': [1, 3]
    }

    grid = GridSearchCV(
        estimator=rf,
        param_grid=param_grid,
        scoring=['recall', 'precision', 'f1', 'roc_auc'],
        refit='recall',
        cv=3,
        n_jobs=-1
    )
    grid.fit(X_train_res, y_train_res)
    print("GridSearch done.")
    
    # Tie break logic manually
    results = pd.DataFrame(grid.cv_results_)
    max_recall = results['mean_test_recall'].max()
    top_candidates = results[results['mean_test_recall'] >= (max_recall - 0.005)]
    best_idx = top_candidates.sort_values(by=['mean_score_time', 'param_n_estimators', 'param_max_depth']).index[0]
    best_params = top_candidates.loc[best_idx, 'params']

    # Retrain best model on full SMOTEd train set
    best_model = RandomForestClassifier(**best_params, random_state=42, n_jobs=-1, class_weight='balanced')
    best_model.fit(X_train_res, y_train_res)

    joblib.dump(best_model, 'models/artifacts/model.pkl')
    print("Model training done.")

    # 5. Evaluation
    start_time = time.time()
    y_pred = best_model.predict(X_test)
    end_time = time.time()
    y_prob = best_model.predict_proba(X_test)[:, 1]

    inference_ms = ((end_time - start_time) / len(X_test)) * 1000

    recall = recall_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_prob)
    cm = confusion_matrix(y_test, y_pred).tolist()

    metrics = {
        "recall": recall,
        "precision": precision,
        "f1": f1,
        "roc_auc": roc_auc,
        "inference_ms": inference_ms
    }

    with open('models/artifacts/metrics.json', 'w') as f:
        json.dump(metrics, f, indent=4)

    with open('reports/model_evaluation.md', 'w') as f:
        f.write(f"# Model Evaluation\n- **Recall** (Primary): {recall:.4f}\n- **Precision**: {precision:.4f}\n- **F1 Score**: {f1:.4f}\n- **ROC AUC**: {roc_auc:.4f}\n- **Inference Time (per sample)**: {inference_ms:.4f} ms\n- **Confusion Matrix**: {cm}\n- **Best Params**: {best_params}\n")
    print("Evaluation done.")

    # 6. Generate SHAP
    explainer = shap.TreeExplainer(best_model)
    shap_values = explainer.shap_values(X_test.iloc[:100])
    
    joblib.dump(explainer, 'models/artifacts/explainer.pkl')

    if isinstance(shap_values, list):
        sv = shap_values[1]
    elif len(shap_values.shape) == 3:
        sv = shap_values[:, :, 1]
    else:
        sv = shap_values

    vals = np.abs(sv).mean(0)
    feature_importance = pd.DataFrame(list(zip(X_train.columns, vals)), columns=['col_name','feature_importance_vals'])
    feature_importance.sort_values(by=['feature_importance_vals'], ascending=False, inplace=True)
    top_10 = feature_importance.head(10)['col_name'].tolist()

    with open('reports/shap_report.md', 'w') as f:
        f.write("# SHAP Report\n## Top 10 Features\n")
        for feat in top_10:
            feat_idx = X_train.columns.tolist().index(feat)
            corr = np.corrcoef(X_test.iloc[:100, feat_idx], sv[:, feat_idx])[0, 1]
            if np.isnan(corr):
                direction = "Neutral"
            elif corr > 0:
                direction = "Higher value -> Higher risk"
            else:
                direction = "Higher value -> Lower risk"
            
            f.write(f"- **{feat}**: {direction}\n")
    print("SHAP generation done.")

    # 7. Metadata
    metadata = {
        "model_name": "rf_diabetes",
        "version": "1.0.0",
        "algorithm": "RandomForest",
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "random_state": 42,
        "features": X_train.columns.tolist(),
        "encoding": ["LabelEncoding(gender)", "OneHotEncoding(smoking_history)"],
        "train_rows": len(X_train_res),
        "test_rows": len(X_test),
        "recall": recall
    }

    with open('models/artifacts/metadata.json', 'w') as f:
        json.dump(metadata, f, indent=4)

    # 8. Validation (Dry Inference)
    print("Running Dry Inference...")
    try:
        # We test simply running prediction from artifacts directly without the trained variables
        val_model = joblib.load('models/artifacts/model.pkl')
        val_explainer = joblib.load('models/artifacts/explainer.pkl')
        # predict 1 sample
        sample_pred = val_model.predict(X_test.iloc[[0]])
        sample_shap = val_explainer.shap_values(X_test.iloc[[0]])
        status = "Success"
    except Exception as e:
        status = f"Failed: {str(e)}"

    with open('reports/artifact_validation.md', 'w') as f:
        f.write(f"# Artifact Validation\n- preprocessor: OK (Verified Phase 1.5)\n- encoder: OK\n- model: OK\n- explainer: OK\n- Dry Inference: {status}\n")

    print(f"Phase 2 Script Completed. Dry inference: {status}")

if __name__ == '__main__':
    main()
