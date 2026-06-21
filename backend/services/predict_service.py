import pandas as pd
from backend.schemas.request import PredictRequest
from backend.startup.load_artifacts import ArtifactStore
from backend.services.formatter_service import format_prediction_response, format_explain_response

def run_pipeline(request: PredictRequest):
    data = request.model_dump()
    df = pd.DataFrame([data])
    
    # Reorder according to metadata
    feature_order = ArtifactStore.metadata.get('feature_order', df.columns.tolist())
    df = df[feature_order]
    
    encoder = ArtifactStore.encoder
    
    # Apply encoding
    df['gender'] = df['gender'].map(encoder['gender_map']).fillna(0)
    
    smoking_test = encoder['smoking_ohe'].transform(df[['smoking_history']])
    smoking_test_df = pd.DataFrame(smoking_test, columns=encoder['smoking_cols'], index=df.index)
    df = pd.concat([df.drop(columns=['smoking_history']), smoking_test_df], axis=1)
    
    # Predict
    prob = ArtifactStore.model.predict_proba(df)[:, 1][0]
    
    # SHAP
    shap_values = ArtifactStore.explainer.shap_values(df, check_additivity=False)
    if isinstance(shap_values, list):
        sv = shap_values[1][0]
    elif len(shap_values.shape) == 3:
        sv = shap_values[0, :, 1]
    else:
        sv = shap_values[0]
        
    return prob, sv.tolist(), df.columns.tolist()

def get_prediction(request: PredictRequest):
    prob, shap_vals, features = run_pipeline(request)
    threshold = ArtifactStore.metadata.get('decision_threshold', 0.40)
    return format_prediction_response(prob, threshold, shap_vals, features)

def get_explanation(request: PredictRequest):
    prob, shap_vals, features = run_pipeline(request)
    return format_explain_response(shap_vals, features)
