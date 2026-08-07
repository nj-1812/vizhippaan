import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from catboost import CatBoostClassifier, Pool

from app.config import settings
from app.services.feature_engineering import engineer_features


RISK_SEVERITY = {"Low": 0.0, "Medium": 1 / 3, "High": 2 / 3, "Critical": 1.0}


class ModelService:
    def __init__(self):
        self.model: CatBoostClassifier | None = None
        self.features: list[str] = []
        self.categorical: list[str] = []
        self.risk_classes: list[str] = []
        self.metrics: dict[str, Any] = {}
        self.loaded = False
        self.error: str | None = None
        self._load()

    def _load(self):
        try:
            model_path = Path(settings.MODEL_PATH)
            metadata_path = Path(settings.METADATA_PATH)
            if not model_path.exists():
                raise FileNotFoundError(f"Model not found: {model_path}")
            if not metadata_path.exists():
                raise FileNotFoundError(f"Metadata not found: {metadata_path}")

            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            self.features = metadata.get("features", [])
            self.categorical = metadata.get("categorical_features", metadata.get("categorical", []))
            self.risk_classes = metadata.get("risk_classes", [])
            self.metrics = metadata.get("metrics", {})

            if not self.features:
                raise ValueError("model_metadata.json does not contain a non-empty 'features' list")

            self.model = CatBoostClassifier()
            self.model.load_model(str(model_path))

            model_classes = [str(x) for x in getattr(self.model, "classes_", [])]
            if model_classes:
                self.risk_classes = model_classes

            self.loaded = True
            self.error = None
        except Exception as exc:
            self.loaded = False
            self.error = str(exc)

    def status(self) -> dict[str, Any]:
        return {
            "loaded": self.loaded,
            "error": self.error,
            "model_path": settings.MODEL_PATH,
            "feature_count": len(self.features),
            "categorical_count": len(self.categorical),
            "classes": self.risk_classes,
            "metrics": self.metrics,
        }

    def _prepare(self, rows: list[dict[str, Any]] | pd.DataFrame) -> pd.DataFrame:
        if not self.loaded or self.model is None:
            raise RuntimeError(self.error or "Model is not loaded")

        df = pd.DataFrame(rows) if not isinstance(rows, pd.DataFrame) else rows.copy()
        df = engineer_features(df)

        missing = [c for c in self.features if c not in df.columns]
        if missing:
            raise ValueError(
                "Missing model features: " + ", ".join(missing[:25])
                + (f" ... (+{len(missing)-25} more)" if len(missing) > 25 else "")
            )

        X = df[self.features].copy()
        categorical_set = set(self.categorical)

        for col in self.features:
            if col in categorical_set:
                X[col] = X[col].where(X[col].notna(), "Unknown").astype(str)
            else:
                # CatBoost natively supports missing numerical values. Preserve NaN
                # so single-student predictions match the model's training behavior.
                X[col] = pd.to_numeric(X[col], errors="coerce")
        return X

    def _probability_payload(self, probs: np.ndarray) -> dict[str, float]:
        return {
            str(cls): round(float(p), 6)
            for cls, p in zip(self.risk_classes, probs)
        }

    def _risk_score(self, probabilities: dict[str, float]) -> float:
        score = sum(RISK_SEVERITY.get(level, 0.0) * p for level, p in probabilities.items())
        return max(0.0, min(1.0, float(score)))

    def predict_rows(self, rows: list[dict[str, Any]] | pd.DataFrame) -> list[dict[str, Any]]:
        X = self._prepare(rows)
        labels = self.model.predict(X).reshape(-1)
        probabilities = self.model.predict_proba(X)

        results = []
        for label, probs in zip(labels, probabilities):
            prob_map = self._probability_payload(probs)
            level = str(label)
            confidence = float(np.max(probs))
            risk_score = self._risk_score(prob_map)
            results.append({
                "risk_level": level,
                "confidence": round(confidence, 6),
                "confidence_percent": round(confidence * 100, 2),
                "risk_score": round(risk_score, 6),
                "risk_percent": round(risk_score * 100, 2),
                # Compatibility key used by the intervention simulator.
                # For this multi-class classifier this is a severity-weighted risk score,
                # not a binary dropout probability.
                "dropout_probability": round(risk_score, 6),
                "class_probabilities": prob_map,
            })
        return results

    def predict_one(self, features: dict[str, Any]) -> dict[str, Any]:
        result = self.predict_rows([features])[0]
        try:
            explanation = self.explain_one(features, top_k=8, class_name=result["risk_level"])
            result["top_factors"] = explanation["top_factors"]
        except Exception:
            result["top_factors"] = []
        return result

    def explain_one(self, features: dict[str, Any], top_k: int = 10, class_name: str | None = None) -> dict[str, Any]:
        X = self._prepare([features])
        pool = Pool(X, cat_features=self.categorical)
        shap = np.asarray(self.model.get_feature_importance(pool, type="ShapValues"))

        # CatBoost MultiClass SHAP shape: [rows, classes, features + 1].
        if shap.ndim == 3:
            predicted = str(self.model.predict(X).reshape(-1)[0])
            target_class = class_name or predicted
            try:
                class_index = self.risk_classes.index(target_class)
            except ValueError:
                class_index = int(np.argmax(self.model.predict_proba(X)[0]))
                target_class = self.risk_classes[class_index]
            values = shap[0, class_index, :-1]
            base_value = float(shap[0, class_index, -1])
        else:
            target_class = class_name or str(self.model.predict(X).reshape(-1)[0])
            values = shap[0][:-1]
            base_value = float(shap[0][-1])

        pairs = sorted(
            zip(self.features, values, X.iloc[0].tolist()),
            key=lambda x: abs(float(x[1])), reverse=True
        )[:top_k]
        return {
            "explained_class": target_class,
            "base_value": round(base_value, 6),
            "top_factors": [
                {
                    "feature": f,
                    "value": None if pd.isna(v) else (v.item() if hasattr(v, "item") else v),
                    "shap_value": round(float(s), 6),
                    "direction": "supports_class" if float(s) > 0 else "opposes_class",
                    "impact": round(abs(float(s)), 6),
                }
                for f, s, v in pairs
            ],
        }

    def global_feature_importance(self, df: pd.DataFrame, top_k: int = 15) -> list[dict[str, Any]]:
        X = self._prepare(df)
        sample = X.sample(min(1000, len(X)), random_state=42) if len(X) else X
        if sample.empty:
            return []
        pool = Pool(sample, cat_features=self.categorical)
        values = self.model.get_feature_importance(pool, type="FeatureImportance")
        pairs = sorted(zip(self.features, values), key=lambda x: float(x[1]), reverse=True)[:top_k]
        total = sum(float(v) for _, v in pairs) or 1.0
        return [
            {"feature": f, "importance": round(float(v), 4), "percent": round(float(v) / total * 100, 2)}
            for f, v in pairs
        ]


model_service = ModelService()
