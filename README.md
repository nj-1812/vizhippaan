# 👁️ VIZHIPPAAN – AI Child Education Risk Intelligence Platform

> **Empowering Early Intervention Through Explainable Artificial Intelligence**

VIZHIPPAAN (விழிப்பான்) is an AI-powered Child Education Risk Intelligence Platform designed to identify students at risk of educational disengagement using academic, attendance, behavioral, family, and socioeconomic indicators.

The platform combines **Machine Learning, Explainable AI (SHAP), Decision Intelligence, and Interactive Analytics** to enable educators and policymakers to proactively support vulnerable students through data-driven interventions.

---

# 🚀 Features

## 📊 AI Risk Prediction
- CatBoost-powered dropout risk prediction
- Student-level probability scoring
- Four-level risk classification
  - 🟢 Low
  - 🟡 Medium
  - 🟠 High
  - 🔴 Critical

---

## 🧠 Explainable AI (XAI)

Every prediction includes transparent explanations using SHAP.

Provides

- Feature Importance
- Prediction Explanation
- Student Risk Drivers
- Responsible AI Transparency

---

## 👤 Student Digital Twin

Complete 360° student intelligence profile

Includes

- Academic Performance
- Attendance History
- Behaviour
- Family Background
- Socioeconomic Factors
- AI Risk History
- Intervention Timeline

---

## 🎯 Intervention Simulator

Simulates intervention strategies before implementation.

Examples

- Scholarship
- Counselling
- Meal Programs
- Digital Access Support
- Attendance Improvement
- NGO Support

Returns estimated changes in predicted student risk.

---

## 🗺 District Risk Intelligence

Interactive district-level analytics including

- Risk Distribution
- Heatmaps
- Student Counts
- District Comparison
- Regional Trends

---

## ⚖ Responsible AI

Built with Responsible AI principles

- SHAP Explainability
- Fairness Monitoring
- Bias Analysis
- Transparent Predictions
- Privacy-Oriented Design

---

## 📈 Decision Intelligence Dashboard

Executive dashboard containing

- Student Overview
- Risk Distribution
- Risk Trends
- Top Risk Factors
- Early Warnings
- Intervention Impact
- Resource Allocation
- Policy Analytics

---

# 🏗 System Architecture

```text
                    Student Dataset
                           │
                           ▼
              Data Cleaning & Validation
                           │
                           ▼
                Feature Engineering Layer
                           │
                           ▼
                CatBoost ML Prediction Model
                           │
            ┌──────────────┴──────────────┐
            ▼                             ▼
     SHAP Explainability         Risk Classification
            │                             │
            └──────────────┬──────────────┘
                           ▼
                 FastAPI Backend Services
                           │
                   REST API Endpoints
                           │
                           ▼
              Next.js Interactive Dashboard
                           │
                           ▼
      Teachers • Schools • District Officials • Policymakers
```

---

# 🛠 Technology Stack

## Frontend

- Next.js 16
- React 19
- TypeScript
- Tailwind CSS
- Recharts
- Framer Motion
- Lucide Icons

---

## Backend

- FastAPI
- Pydantic
- Uvicorn
- Pandas
- NumPy

---

## Artificial Intelligence

- CatBoost
- SHAP
- Scikit-learn

---

## Data Processing

- Feature Engineering
- Risk Scoring
- Explainable AI
- Counterfactual Simulation

---

# 📂 Project Structure

```text
VIZHIPPAAN
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── public/
│   ├── lib/
│   └── package.json
│
└── backend/
    │
    ├── app/
    │   ├── routers/
    │   ├── services/
    │   ├── utils/
    │   ├── schemas.py
    │   ├── config.py
    │   └── main.py
    │
    ├── models/
    │   ├── vizhippaan_catboost_model.cbm
    │   └── model_metadata.json
    │
    ├── data/
    │   └── vizhippaan_feature_engineered.csv
    │
    ├── requirements.txt
    ├── Dockerfile
    ├── render.yaml
    └── README.md
```

---

# ⚙ Installation

## 1. Clone Repository

```bash
git clone https://github.com/<your-username>/vizhippaan.git
cd vizhippaan
```

---

## 2. Create Virtual Environment

```bash
cd backend

python -m venv .venv
```

Windows

```powershell
.venv\Scripts\Activate.ps1
```

Linux / macOS

```bash
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment

Copy

```text
.env.example
```

to

```text
.env
```

Configure

```env
FRONTEND_ORIGINS=http://localhost:3000
```

When deploying, replace it with your frontend URL.

Example

```env
FRONTEND_ORIGINS=https://vizhippaan.vercel.app
```

---

# 📦 Required Model Files

Copy the exported files from your training pipeline.

```text
backend/models/
│
├── vizhippaan_catboost_model.cbm
└── model_metadata.json

backend/data/
│
└── vizhippaan_feature_engineered.csv
```

These files are required for model inference and dashboard analytics.

---

# ▶ Running the Backend

```bash
uvicorn app.main:app --reload --port 8000
```

Backend

```
http://127.0.0.1:8000
```

Swagger Documentation

```
http://127.0.0.1:8000/docs
```

Health Check

```
http://127.0.0.1:8000/api/health
```

---

# 📡 API Endpoints

## Dashboard

```
GET /api/dashboard/overview
GET /api/dashboard/summary
GET /api/dashboard/risk-trend
GET /api/dashboard/top-risk-factors
GET /api/dashboard/alerts
```

---

## Student Intelligence

```
GET /api/students
GET /api/students/{student_id}
GET /api/students/{student_id}/risk
GET /api/students/{student_id}/digital-twin
GET /api/students/{student_id}/explanation
```

---

## Prediction

```
POST /api/predict
POST /api/predict/batch
```

---

## Intervention Intelligence

```
POST /api/interventions/simulate
```

---

## District Analytics

```
GET /api/districts/risk
```

---

## Responsible AI

```
GET /api/fairness/report
```

---

## Resource Intelligence

```
GET /api/resources/allocation
```

---

## Early Warning

```
GET /api/early-warning
```

---

## Policy Intelligence

```
POST /api/policy/simulate
```

---

## System Health

```
GET /api/health
GET /api/quality
```

---

# 🎯 Prediction Pipeline

```text
Student Data
      │
      ▼
Data Validation
      │
      ▼
Feature Engineering
      │
      ▼
CatBoost Prediction
      │
      ▼
Probability Score
      │
      ▼
Risk Classification
      │
      ▼
SHAP Explainability
      │
      ▼
Intervention Recommendation
      │
      ▼
Dashboard Analytics
```

---

# 📊 Risk Classification

| Probability | Risk Level |
|-------------|------------|
| ≤ 0.6589 | 🟢 Low |
| ≤ 0.9224 | 🟡 Medium |
| ≤ 0.9831 | 🟠 High |
| > 0.9831 | 🔴 Critical |

---

# 🔒 Responsible AI

VIZHIPPAAN follows responsible AI practices through

- Explainable Predictions
- SHAP-based Transparency
- Fairness Monitoring
- Privacy-Conscious Design
- Human-Centered Decision Support

---

# ⚠ Disclaimer

The Intervention Simulator provides **counterfactual scenario simulations** based on changes to selected student attributes. These estimates are intended to support planning and decision-making and **should not be interpreted as proof of causal impact**. Final intervention decisions should always involve educators and domain experts.

---

# 🌍 Future Scope

- Real-Time Data Integration
- GIS-Based Risk Intelligence
- Mobile Application
- Multilingual AI Assistant
- Offline-First Support
- Predictive Policy Analytics
- AI-Powered Recommendation Engine
- Statewide & Nationwide Deployment

---

# 👨‍💻 Developed For

**DATASPHERE '26**

**Track 5 – AI for Social Good**

**Project:** VIZHIPPAAN (விழிப்பான்)

*Empowering Every Child Through Responsible Artificial Intelligence.*
