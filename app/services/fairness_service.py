import pandas as pd
from app.services.data_service import data_service


def fairness_report() -> dict:
    df = data_service.dataframe().copy()
    if df.empty:
        return {"groups": [], "summary": {"status": "unavailable"}}
    risk = data_service._risk_series(df)
    high = risk.isin(["High", "Critical"]).astype(int)
    dimensions = [c for c in ["gender", "location_type", "grade_level"] if c in df.columns]
    reports=[]
    worst_gap=0.0
    for col in dimensions:
        temp=pd.DataFrame({"group":df[col].astype(str), "high":high})
        rates=temp.groupby("group")["high"].agg(["mean","count"]).reset_index()
        rates=rates[rates["count"] >= 5]
        if rates.empty: continue
        gap=float(rates["mean"].max()-rates["mean"].min())*100
        worst_gap=max(worst_gap,gap)
        reports.append({
            "dimension":col,
            "parity_difference_pct":round(gap,2),
            "groups":[{"name":r["group"],"high_risk_rate_pct":round(float(r["mean"])*100,2),"count":int(r["count"])} for _,r in rates.iterrows()]
        })
    status="Good" if worst_gap <= 5 else "Review" if worst_gap <= 10 else "Attention"
    return {"summary":{"worst_parity_difference_pct":round(worst_gap,2),"status":status,"dimensions_monitored":len(reports)},"groups":reports}
