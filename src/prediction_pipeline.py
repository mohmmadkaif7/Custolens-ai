
import os
import joblib
import pandas as pd
import numpy as np

from src.recommendation_engine import generate_recommendations

MODEL_PATH = os.path.join(
    os.path.dirname(__file__), "..", "data", "customer_segmentation_model.pkl"
)

model = joblib.load(MODEL_PATH)
FEATURES = ["age", "income", "purchase_frequency", "annual_spending"]

def predict_customer_segment(age, income, purchase_frequency, annual_spending):
    customer = pd.DataFrame({
        "age": [age],
        "income": [income],
        "purchase_frequency": [purchase_frequency],
        "annual_spending": [annual_spending]
    })
    return model.predict(customer)[0]

def predict_customer_details(age, income, purchase_frequency, annual_spending, reference_df=None):
    customer = pd.DataFrame({
        "age": [age],
        "income": [income],
        "purchase_frequency": [purchase_frequency],
        "annual_spending": [annual_spending]
    })
    segment = model.predict(customer)[0]

    probabilities = {}
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(customer)[0]
        probabilities = {str(cls): float(prob) for cls, prob in zip(model.classes_, probs)}
    confidence = probabilities.get(str(segment), 1.0)

    # Local sensitivity: temporarily reset one feature to the training median.
    # A positive value means the feature was supporting the selected class.
    baseline = confidence
    contributions = []
    if reference_df is not None and all(c in reference_df.columns for c in FEATURES):
        medians = reference_df[FEATURES].median(numeric_only=True)
        for feature in FEATURES:
            changed = customer.copy()
            changed.loc[0, feature] = medians[feature]
            if hasattr(model, "predict_proba"):
                new_prob = float(model.predict_proba(changed)[0][list(model.classes_).index(segment)])
                support = baseline - new_prob
            else:
                new_prob = baseline
                support = 0.0
            contributions.append({
                "feature": feature,
                "support": support,
                "value": float(customer.loc[0, feature]),
                "median": float(medians[feature]),
            })

    contributions.sort(key=lambda x: x["support"], reverse=True)

    recommendation_result = generate_recommendations(segment)
    return {
        "segment": segment,
        "confidence": confidence,
        "probabilities": probabilities,
        "contributions": contributions,
        "strategy": recommendation_result.get("strategy", "General customer engagement"),
        "recommendations": recommendation_result.get("recommendations", []),
    }

def analyze_customer(age, income, purchase_frequency, annual_spending):
    result = predict_customer_details(age, income, purchase_frequency, annual_spending)
    return result
