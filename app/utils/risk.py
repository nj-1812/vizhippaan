RISK_ORDER = ["Low", "Medium", "High", "Critical"]

# Exact thresholds used in the final Colab CatBoost pipeline.
def probability_to_risk(score: float) -> str:
    score = max(0.0, min(1.0, float(score)))
    if score <= 0.6589:
        return "Low"
    if score <= 0.9224:
        return "Medium"
    if score <= 0.9831:
        return "High"
    return "Critical"


def risk_severity(level: str) -> int:
    try:
        return RISK_ORDER.index(str(level).title())
    except ValueError:
        return -1
