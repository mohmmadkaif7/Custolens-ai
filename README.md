# CustoLens AI

CustoLens AI is an AI-powered customer intelligence platform for customer segmentation, prediction, analytics and business strategy.

## New UI

The Streamlit application now uses a professional dark-blue/purple sidebar with icons and these pages:

- Home
- Dashboard
- Customer Prediction
- Batch Analysis
- Analytics
- Business Strategies
- API & Integration
- About

The old Customer Data page has been removed from navigation. Customer filtering is now part of Batch Analysis and operates on the uploaded CSV.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

Optional API:

```bash
uvicorn api:app --reload --port 8000
```

## Main ML flow

1. Customer segmentation
2. Random Forest segment prediction
3. Local prediction explanation
4. Business strategy recommendations

## Batch Analysis

Upload a CSV and the application will:

- detect supported customer columns
- validate model-ready fields
- provide filters for the uploaded data
- show interactive charts for the uploaded data
- predict Premium / Regular / Budget
- show result counts
- allow CSV download

## Prediction Explainability

The Customer Prediction page shows the predicted segment beside the profile, model confidence, segment benchmark comparisons and local feature-support signals.


## 🧪 Testing

CustoLens AI includes automated tests using **pytest** covering:

- Data validation and adaptation
- ML prediction and probabilities
- Business recommendations
- FastAPI endpoints
- Invalid input handling

Run the complete test suite with:

```bash
pytest -v