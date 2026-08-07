from copy import deepcopy
from typing import Any
from app.services.model_service import model_service

# Interventions modify model inputs, then the CatBoost model is re-run.
# This is a scenario simulator, not a claim of causal treatment effect.
INTERVENTIONS = {
    "scholarship": {"scholarship_received": True},
    "free_meal": {"free_meal_program_enrolled": True},
    "ngo_support": {"ngo_intervention_present": True},
    "literacy_program": {"literacy_program_enrolled": True},
    "extracurricular": {"extracurricular_participation": True},
    "internet_access": {"household_has_internet_access": True},
    "device_access": {"owns_smartphone_or_computer": True},
    "attendance_support": {"attendance_rate_pct": ("increase", 10, 100)},
    "remedial_classes": {"average_test_score_pct": ("increase", 10, 100)},
}


def apply_interventions(features: dict[str, Any], interventions: list[str]) -> dict[str, Any]:
    updated = deepcopy(features)
    for name in interventions:
        patch = INTERVENTIONS.get(name)
        if not patch:
            continue
        for key, value in patch.items():
            if isinstance(value, tuple) and value[0] == "increase":
                current = float(updated.get(key, 0) or 0)
                updated[key] = min(float(value[2]), current + float(value[1]))
            else:
                updated[key] = value
    return updated


def simulate(features: dict[str, Any], interventions: list[str]):
    before = model_service.predict_one(features)
    changed = apply_interventions(features, interventions)
    after = model_service.predict_one(changed)
    reduction = before["dropout_probability"] - after["dropout_probability"]
    return {
        "interventions": interventions,
        "before": before,
        "after": after,
        "absolute_probability_reduction": round(reduction, 6),
        "relative_risk_reduction_percent": round((reduction / before["dropout_probability"] * 100), 2) if before["dropout_probability"] else 0,
        "modified_features": {k: changed[k] for k in changed if changed.get(k) != features.get(k)},
        "method_note": "Counterfactual model scenario; not a causal treatment-effect estimate.",
    }
