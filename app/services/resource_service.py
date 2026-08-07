from app.services.data_service import data_service


def allocation_plan(budget: float = 100000, district: str | None = None):
    summary = data_service.summary(district)
    high = summary["risk"].get("High", {}).get("count", 0)
    critical = summary["risk"].get("Critical", {}).get("count", 0)
    priority = high + 2 * critical
    if priority <= 0:
        return {"budget":budget,"district":district,"allocations":[]}

    # Demonstration optimizer weights. Replace costs/constraints with official program data when available.
    weights = {
        "Scholarships": 0.35,
        "Counsellors": 0.25,
        "Devices": 0.20,
        "Meals": 0.20,
    }
    unit_cost = {"Scholarships": 100, "Counsellors": 1200, "Devices": 180, "Meals": 30}
    items=[]
    for name,w in weights.items():
        amount=budget*w
        items.append({"resource":name,"allocated_budget":round(amount,2),"estimated_units":int(amount/unit_cost[name]),"priority_weight":w})
    return {"district":district or "All Districts","budget":budget,"priority_score":priority,"allocations":items,"method_note":"Heuristic budget allocator for demo; configure real unit costs before operational use."}
