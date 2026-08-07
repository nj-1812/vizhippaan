# VIZHIPPAAN — Run Locally

This package already contains the trained CatBoost classifier, model metadata, feature-engineered dataset, feature-importance CSV, FastAPI backend, and Next.js dashboard integration helper.

## Terminal 1 — Backend

From the project root in VS Code PowerShell:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env -Force
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Verify:

- API health: `http://127.0.0.1:8000/api/health`
- Swagger docs: `http://127.0.0.1:8000/docs`

A healthy response should report the CatBoost model as loaded and the dataset as 200,000 rows.

## Terminal 2 — Frontend

Open a second terminal in the same project root:

```powershell
npm install
$env:NEXT_PUBLIC_API_URL="http://127.0.0.1:8000/api"
npm run dev
```

Then open:

`http://localhost:3000`

The Overview dashboard is wired to request live summary, trend, feature-importance, and model-health data from FastAPI. If the backend is unavailable it keeps the existing visual fallback values instead of crashing the UI.

## Important included files

```text
models/vizhippaan_catboost_model.cbm
models/model_metadata.json
data/vizhippaan_feature_engineered.csv
data/vizhippaan_feature_importance.csv
lib/api.ts
```

## Useful API endpoints

```text
GET  /api/health
GET  /api/dashboard/overview
GET  /api/dashboard/summary
GET  /api/dashboard/risk-trend
GET  /api/dashboard/top-risk-factors
GET  /api/students?limit=50
GET  /api/students/{student_id}/risk
GET  /api/students/{student_id}/explanation
GET  /api/students/{student_id}/digital-twin
POST /api/predict
POST /api/predict/batch
POST /api/interventions/simulate
GET  /api/fairness/report
GET  /api/districts/risk
```

## Model note

The exported model is a CatBoost **multi-class classifier** with classes `Critical`, `High`, `Low`, and `Medium`. The backend uses `predict_proba()` for class confidence and class-specific SHAP values for explanations. `risk_score` is a severity-weighted 0–1 score derived from the four class probabilities; it should not be described as a calibrated binary dropout probability.
