from typing import Any, Dict, List

from app.schemas.digital_twin import (
    DigitalTwinRequest,
)

from app.services.model_service import (
    model_service,
)


class DigitalTwinService:

    @staticmethod
    def _risk_level(
        probability: float,
    ) -> str:
        if probability < 25:
            return "Low"

        if probability < 50:
            return "Medium"

        if probability < 75:
            return "High"

        return "Critical"

    @staticmethod
    def _attendance_status(
        attendance: float,
    ) -> str:
        if attendance >= 85:
            return "Stable"

        if attendance >= 70:
            return "Needs Attention"

        return "High Concern"

    @staticmethod
    def _academic_status(
        score: float,
    ) -> str:
        if score >= 75:
            return "Strong"

        if score >= 60:
            return "Moderate"

        if score >= 40:
            return "Needs Support"

        return "Critical Support Required"

    @staticmethod
    def _economic_status(
        income: float,
    ) -> str:
        if income >= 50000:
            return "Relatively Stable"

        if income >= 25000:
            return "Moderate Vulnerability"

        return "High Vulnerability"

    @staticmethod
    def _risk_factors(
        data: DigitalTwinRequest,
    ) -> List[Dict[str, Any]]:

        factors = []

        if data.attendance_rate < 75:
            factors.append({
                "factor": "Low Attendance",
                "value": f"{data.attendance_rate:.1f}%",
                "impact": "High",
                "contribution": round(
                    min(
                        100,
                        (75 - data.attendance_rate) * 2,
                    ),
                    2,
                ),
            })

        if data.average_test_score < 60:
            factors.append({
                "factor": "Low Academic Performance",
                "value": f"{data.average_test_score:.1f}%",
                "impact": "High",
                "contribution": round(
                    min(
                        100,
                        (60 - data.average_test_score) * 1.5,
                    ),
                    2,
                ),
            })

        if data.household_income < 25000:
            factors.append({
                "factor": "Low Household Income",
                "value": f"₹{data.household_income:,.0f}",
                "impact": "Medium",
                "contribution": round(
                    min(
                        100,
                        (25000 - data.household_income) / 250,
                    ),
                    2,
                ),
            })

        if data.distance_to_school > 5:
            factors.append({
                "factor": "Long Distance to School",
                "value": f"{data.distance_to_school:.1f} km",
                "impact": "Medium",
                "contribution": round(
                    min(
                        100,
                        (data.distance_to_school - 5) * 5,
                    ),
                    2,
                ),
            })

        if not data.internet_access:
            factors.append({
                "factor": "No Internet Access",
                "value": "Unavailable",
                "impact": "Medium",
                "contribution": 25.0,
            })

        if data.behavioural_incidents > 0:
            factors.append({
                "factor": "Behavioural Incidents",
                "value": str(
                    data.behavioural_incidents
                ),
                "impact": "Medium",
                "contribution": round(
                    min(
                        100,
                        data.behavioural_incidents * 12,
                    ),
                    2,
                ),
            })

        factors.sort(
            key=lambda item: item["contribution"],
            reverse=True,
        )

        return factors[:5]

    @staticmethod
    def _recommendation(
        data: DigitalTwinRequest,
    ) -> str:

        recommendations = []

        if data.attendance_rate < 75:
            recommendations.append(
                "initiate attendance monitoring and parent outreach"
            )

        if data.average_test_score < 60:
            recommendations.append(
                "provide remedial academic support"
            )

        if data.household_income < 25000:
            recommendations.append(
                "assess scholarship or welfare eligibility"
            )

        if data.distance_to_school > 5:
            recommendations.append(
                "evaluate transport support"
            )

        if not data.internet_access:
            recommendations.append(
                "provide digital learning access"
            )

        if data.behavioural_incidents > 1:
            recommendations.append(
                "schedule counselling or mentoring"
            )

        if not recommendations:
            return (
                "Student indicators are currently stable. "
                "Continue routine monitoring."
            )

        return (
            "Recommended action: "
            + "; ".join(recommendations)
            + "."
        )

    def generate(
        self,
        data: DigitalTwinRequest,
    ) -> Dict[str, Any]:

        # =====================================================
        # REAL MODEL INPUT
        # =====================================================

        model_input = {
            "attendance_rate":
                data.attendance_rate,

            "average_test_score":
                data.average_test_score,

            "household_income":
                data.household_income,

            "distance_to_school":
                data.distance_to_school,

            "internet_access":
                data.internet_access,

            "behavioural_incidents":
                data.behavioural_incidents,
        }

        prediction = model_service.predict(
            model_input
        )

        probability = float(
            prediction.get(
                "dropout_probability",
                0,
            )
        )

        # Supports both 0.62 and 62 formats
        if probability <= 1:
            probability *= 100

        probability = round(
            max(
                0,
                min(
                    100,
                    probability,
                ),
            ),
            2,
        )

        risk_level = prediction.get(
            "predicted_risk"
        ) or self._risk_level(
            probability
        )

        confidence = float(
            prediction.get(
                "confidence_score",
                0,
            )
        )

        if confidence <= 1:
            confidence *= 100

        confidence = round(
            max(
                0,
                min(
                    100,
                    confidence,
                ),
            ),
            2,
        )

        student_id = (
            data.student_id
            or "LIVE-STUDENT"
        )

        return {
            "student_id":
                student_id,

            "risk_probability":
                probability,

            "risk_score":
                probability,

            "risk_level":
                risk_level,

            "confidence_score":
                confidence,

            "attendance_rate":
                data.attendance_rate,

            "average_test_score":
                data.average_test_score,

            "household_income":
                data.household_income,

            "distance_to_school":
                data.distance_to_school,

            "internet_access":
                data.internet_access,

            "behavioural_incidents":
                data.behavioural_incidents,

            "academic_status":
                self._academic_status(
                    data.average_test_score
                ),

            "attendance_status":
                self._attendance_status(
                    data.attendance_rate
                ),

            "socioeconomic_status":
                self._economic_status(
                    data.household_income
                ),

            "digital_access_status":
                (
                    "Available"
                    if data.internet_access
                    else "Limited"
                ),

            "top_risk_factors":
                self._risk_factors(
                    data
                ),

            "recommendation":
                self._recommendation(
                    data
                ),

            "engine":
                "VIZHIPPAAN AI Student Digital Twin",
        }


digital_twin_service = DigitalTwinService()
