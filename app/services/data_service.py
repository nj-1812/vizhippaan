from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from app.config import settings
from app.services.feature_engineering import engineer_features
from app.services.model_service import model_service
from app.utils.risk import RISK_ORDER, probability_to_risk

class DataService:
    def __init__(self):
        self.path = Path(settings.DATA_PATH)
        self.error: str | None = None

    @lru_cache(maxsize=1)
    def dataframe(self) -> pd.DataFrame:
        if not self.path.exists():
            self.error = f"Dataset not found: {self.path}"
            return pd.DataFrame()
        try:
            df = pd.read_csv(self.path, low_memory=False)
            df = engineer_features(df)
            self.error = None
            return df
        except Exception as exc:
            self.error = str(exc)
            return pd.DataFrame()

    def reload(self):
        self.dataframe.cache_clear()
        return self.dataframe()

    def status(self):
        df = self.dataframe()
        return {"loaded": not df.empty, "rows": int(len(df)), "columns": int(len(df.columns)), "error": self.error}

    @staticmethod
    def _risk_series(df: pd.DataFrame) -> pd.Series:
        if "predicted_risk" in df.columns:
            return df["predicted_risk"].astype(str).str.title()
        if "dropout_risk_level" in df.columns:
            return df["dropout_risk_level"].astype(str).str.title()
        if "predicted_probability" in df.columns:
            return df["predicted_probability"].apply(probability_to_risk)
        if "dropout_probability_score" in df.columns:
            return df["dropout_probability_score"].apply(probability_to_risk)
        if model_service.loaded and not df.empty:
            try:
                preds = model_service.predict_rows(df)
                return pd.Series([x["risk_level"] for x in preds], index=df.index)
            except Exception:
                pass
        return pd.Series(["Unknown"] * len(df), index=df.index)

    def summary(self, district: str | None = None) -> dict[str, Any]:
        df = self.dataframe().copy()
        if df.empty:
            return {"total_students": 0, "risk": {k: {"count": 0, "percent": 0} for k in RISK_ORDER}}
        district_col = next((c for c in ["district", "district_name", "state_or_province", "state"] if c in df.columns), None)
        if district and district.lower() not in {"all", "all districts"} and district_col:
            df = df[df[district_col].astype(str).str.lower() == district.lower()]
        risk = self._risk_series(df)
        total = len(df)
        result = {}
        for level in RISK_ORDER:
            count = int((risk == level).sum())
            result[level] = {"count": count, "percent": round((count / total * 100) if total else 0, 2)}
        return {"total_students": int(total), "risk": result}

    def student(self, student_id: str) -> dict[str, Any] | None:
        df = self.dataframe()
        if df.empty or "student_id" not in df.columns:
            return None
        rows = df[df["student_id"].astype(str) == str(student_id)]
        if rows.empty:
            return None
        row = rows.iloc[0]
        return {k: (None if pd.isna(v) else v.item() if hasattr(v, "item") else v) for k, v in row.to_dict().items()}

    def student_list(self, q: str = "", risk_level: str | None = None, district: str | None = None, limit: int = 50):
        df = self.dataframe().copy()
        if df.empty:
            return []
        risk = self._risk_series(df)
        df = df.assign(_risk=risk)
        if q and "student_id" in df.columns:
            df = df[df["student_id"].astype(str).str.contains(q, case=False, na=False)]
        if risk_level:
            df = df[df["_risk"].str.lower() == risk_level.lower()]
        district_col = next((c for c in ["district", "district_name", "state_or_province", "state"] if c in df.columns), None)
        if district and district_col:
            df = df[df[district_col].astype(str).str.lower() == district.lower()]
        cols = [c for c in ["student_id", "age", "gender", "grade_level", district_col, "attendance_rate_pct", "average_test_score_pct"] if c and c in df.columns]
        out=[]
        for idx, row in df.head(limit).iterrows():
            item={c:(None if pd.isna(row[c]) else row[c].item() if hasattr(row[c], 'item') else row[c]) for c in cols}
            item["risk_level"] = row["_risk"]
            out.append(item)
        return out

    def risk_trend(self) -> list[dict[str, Any]]:
        df = self.dataframe().copy()
        if df.empty:
            return []
        date_col = next((c for c in ["record_generated_date", "date", "month"] if c in df.columns), None)
        if not date_col:
            return []
        dt = pd.to_datetime(df[date_col], errors="coerce")
        df = df.assign(_date=dt, _risk=self._risk_series(df)).dropna(subset=["_date"])
        if df.empty:
            return []
        df["month"] = df["_date"].dt.to_period("M").astype(str)
        result=[]
        for month, group in df.groupby("month", sort=True):
            total=len(group)
            item={"month":month}
            for level in RISK_ORDER:
                item[level.lower()] = round((group["_risk"] == level).sum()/total*100,2) if total else 0
            result.append(item)
        return result[-12:]

    def districts(self) -> list[dict[str, Any]]:
        df = self.dataframe().copy()
        if df.empty:
            return []
        district_col = next((c for c in ["district", "district_name", "state_or_province", "state", "location_type"] if c in df.columns), None)
        if not district_col:
            return []
        df = df.assign(_risk=self._risk_series(df))
        rows=[]
        for name, g in df.groupby(district_col, dropna=False):
            total=len(g); high=int(g["_risk"].isin(["High","Critical"]).sum())
            critical=int((g["_risk"]=="Critical").sum())
            rows.append({
                "district": str(name), "students": int(total), "high_or_critical": high,
                "critical": critical, "risk_percent": round(high/total*100,2) if total else 0,
            })
        return sorted(rows, key=lambda x:x["risk_percent"], reverse=True)

    def alerts(self):
        df=self.dataframe().copy()
        if df.empty: return []
        risk=self._risk_series(df)
        critical=int((risk=="Critical").sum()); high=int((risk=="High").sum())
        low_att=int((pd.to_numeric(df.get("attendance_rate_pct"), errors="coerce") < 60).sum()) if "attendance_rate_pct" in df.columns else 0
        low_score=int((pd.to_numeric(df.get("average_test_score_pct"), errors="coerce") < 40).sum()) if "average_test_score_pct" in df.columns else 0
        return [
            {"severity":"critical","title":f"{critical:,} students are Critical Risk","detail":"Immediate intervention recommended"},
            {"severity":"high","title":f"{high:,} students are High Risk","detail":"Prioritize counselling and attendance support"},
            {"severity":"warning","title":f"{low_att:,} students have attendance below 60%","detail":"Attendance intervention candidate group"},
            {"severity":"info","title":f"{low_score:,} students have test scores below 40%","detail":"Academic support candidate group"},
        ]

data_service = DataService()
