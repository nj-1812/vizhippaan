import numpy as np
import pandas as pd

VULNERABILITY_FEATURES = [
    "is_orphan",
    "single_parent_household",
    "child_labor_involvement",
    "early_marriage_risk_flag",
    "community_conflict_zone",
    "seasonal_migration_family",
    "language_barrier_flag",
]
DIGITAL_COLUMNS = [
    "household_has_electricity",
    "household_has_internet_access",
    "owns_smartphone_or_computer",
]
SUPPORT_COLUMNS = [
    "scholarship_received",
    "free_meal_program_enrolled",
    "ngo_intervention_present",
    "literacy_program_enrolled",
    "extracurricular_participation",
]


def _bool_to_int(series: pd.Series) -> pd.Series:
    return (
        series.astype(str).str.lower().map({
            "true": 1, "false": 0, "1": 1, "0": 0,
            "yes": 1, "no": 0, "y": 1, "n": 0,
        }).fillna(0).astype(int)
    )


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Recreates the feature engineering used in the Colab pipeline where possible.

    Safe to call on already-engineered data: existing derived columns are overwritten
    consistently when their source columns are present.
    """
    out = df.copy()

    for col in VULNERABILITY_FEATURES:
        if col in out.columns:
            out[col + "_binary"] = _bool_to_int(out[col])
    vuln_bins = [c + "_binary" for c in VULNERABILITY_FEATURES if c + "_binary" in out.columns]
    if vuln_bins:
        out["social_vulnerability_score"] = out[vuln_bins].sum(axis=1)

    for col in DIGITAL_COLUMNS:
        if col in out.columns:
            out[col + "_binary"] = _bool_to_int(out[col])
    digital_bins = [c + "_binary" for c in DIGITAL_COLUMNS if c + "_binary" in out.columns]
    if digital_bins:
        out["digital_access_score"] = out[digital_bins].sum(axis=1)

    for col in SUPPORT_COLUMNS:
        if col in out.columns:
            out[col + "_binary"] = _bool_to_int(out[col])
    support_bins = [c + "_binary" for c in SUPPORT_COLUMNS if c + "_binary" in out.columns]
    if support_bins:
        out["intervention_support_score"] = out[support_bins].sum(axis=1)

    if {"household_income_monthly_usd", "family_size"}.issubset(out.columns):
        family = pd.to_numeric(out["family_size"], errors="coerce").replace(0, np.nan)
        income = pd.to_numeric(out["household_income_monthly_usd"], errors="coerce")
        v = income / family
        med = v.median()
        out["income_per_family_member"] = v.fillna(0 if pd.isna(med) else med)

    if {"attendance_rate_pct", "average_test_score_pct"}.issubset(out.columns):
        att = pd.to_numeric(out["attendance_rate_pct"], errors="coerce")
        test = pd.to_numeric(out["average_test_score_pct"], errors="coerce")
        out["learning_engagement_score"] = (att * test) / 100.0

    if {"record_generated_date", "enrollment_date"}.issubset(out.columns):
        r = pd.to_datetime(out["record_generated_date"], errors="coerce")
        e = pd.to_datetime(out["enrollment_date"], errors="coerce")
        out["enrollment_duration_days"] = (r - e).dt.days

    return out
