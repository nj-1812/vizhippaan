from typing import Any, Dict, List

from app.schemas.student_intelligence import StudentIntelligenceRequest
from app.services.model_service import model_service


class StudentIntelligenceService:
    """
    VIZHIPPAAN Student Intelligence Service

    Provides backend intelligence for:
    1. AI Student Digital Twin
    2. Student Journey Timeline
    3. Risk Explanation
    4. Early Warning Horizon

    Current risk predictions are obtained from the VIZHIPPAAN
    model service. Additional scores, explanations and forecasts
    are derived from the student's current and historical data.
    """

    # =========================================================
    # COMMON HELPERS
    # =========================================================

    @staticmethod
    def _clamp(
        value: float,
        minimum: float = 0.0,
        maximum: float = 100.0,
    ) -> float:
        return max(minimum, min(maximum, value))

    @staticmethod
    def _risk_level(probability: float) -> str:
        if probability < 25:
            return "Low"
        if probability < 50:
            return "Medium"
        if probability < 75:
            return "High"
        return "Critical"

    # =========================================================
    # MODEL PREDICTION
    # =========================================================

    def _predict(
        self,
        attendance_rate: float,
        average_test_score: float,
        household_income: float,
        distance_to_school: float,
        internet_access: bool,
        behavioural_incidents: int,
    ) -> Dict[str, Any]:

        payload = {
            "attendance_rate": attendance_rate,
            "average_test_score": average_test_score,
            "household_income": household_income,
            "distance_to_school": distance_to_school,
            "internet_access": internet_access,
            "behavioural_incidents": behavioural_incidents,
        }

        result = model_service.predict(payload)

        # -----------------------------------------------------
        # Risk probability
        # -----------------------------------------------------

        probability = float(
            result.get(
                "dropout_probability",
                result.get("risk_probability", 0),
            )
        )

        # Support either 0-1 or 0-100 probability formats
        if probability <= 1:
            probability *= 100

        probability = round(
            self._clamp(probability),
            2,
        )

        # -----------------------------------------------------
        # Risk level
        # -----------------------------------------------------

        risk_level = (
            result.get("predicted_risk")
            or result.get("risk_level")
            or self._risk_level(probability)
        )

        # -----------------------------------------------------
        # Confidence
        # -----------------------------------------------------

        confidence = float(
            result.get("confidence_score", 0)
        )

        if confidence <= 1:
            confidence *= 100

        confidence = round(
            self._clamp(confidence),
            2,
        )

        return {
            "probability": probability,
            "risk_level": risk_level,
            "confidence": confidence,
            "raw_prediction": result,
        }

    # =========================================================
    # RISK DRIVER ENGINE
    # =========================================================

    def _risk_drivers(
        self,
        data: StudentIntelligenceRequest,
    ) -> List[Dict[str, Any]]:

        drivers: List[Dict[str, Any]] = []

        # -----------------------------------------------------
        # Attendance
        # -----------------------------------------------------

        if data.attendance_rate < 75:
            impact = self._clamp(
                (75 - data.attendance_rate) * 2
            )

            drivers.append(
                {
                    "factor": "Low Attendance",
                    "impact": round(impact, 2),
                    "type": "risk",
                    "explanation": (
                        f"Attendance is "
                        f"{data.attendance_rate:.1f}%, "
                        "below the preferred 75% threshold."
                    ),
                }
            )

        else:
            impact = min(
                30,
                (data.attendance_rate - 75) * 1.2,
            )

            drivers.append(
                {
                    "factor": "Stable Attendance",
                    "impact": round(impact, 2),
                    "type": "protective",
                    "explanation": (
                        "Attendance currently supports "
                        "continued student engagement."
                    ),
                }
            )

        # -----------------------------------------------------
        # Academic performance
        # -----------------------------------------------------

        if data.average_test_score < 60:
            impact = self._clamp(
                (60 - data.average_test_score) * 1.5
            )

            drivers.append(
                {
                    "factor": "Low Academic Performance",
                    "impact": round(impact, 2),
                    "type": "risk",
                    "explanation": (
                        f"Average academic score is "
                        f"{data.average_test_score:.1f}%."
                    ),
                }
            )

        else:
            impact = min(
                30,
                data.average_test_score - 60,
            )

            drivers.append(
                {
                    "factor": "Academic Stability",
                    "impact": round(impact, 2),
                    "type": "protective",
                    "explanation": (
                        "Academic performance is "
                        "currently stable."
                    ),
                }
            )

        # -----------------------------------------------------
        # Household income
        # -----------------------------------------------------

        if data.household_income < 25000:
            impact = self._clamp(
                (25000 - data.household_income) / 250
            )

            drivers.append(
                {
                    "factor": "Economic Vulnerability",
                    "impact": round(impact, 2),
                    "type": "risk",
                    "explanation": (
                        "Household income may create "
                        "financial barriers to education."
                    ),
                }
            )

        # -----------------------------------------------------
        # Distance to school
        # -----------------------------------------------------

        if data.distance_to_school > 5:
            impact = self._clamp(
                (data.distance_to_school - 5) * 5
            )

            drivers.append(
                {
                    "factor": "Travel Distance",
                    "impact": round(impact, 2),
                    "type": "risk",
                    "explanation": (
                        f"The student travels "
                        f"{data.distance_to_school:.1f} km "
                        "to school."
                    ),
                }
            )

        # -----------------------------------------------------
        # Internet access
        # -----------------------------------------------------

        if not data.internet_access:
            drivers.append(
                {
                    "factor": "No Internet Access",
                    "impact": 25.0,
                    "type": "risk",
                    "explanation": (
                        "Reliable digital learning access "
                        "is unavailable."
                    ),
                }
            )

        # -----------------------------------------------------
        # Behaviour
        # -----------------------------------------------------

        if data.behavioural_incidents > 0:
            impact = min(
                100,
                data.behavioural_incidents * 12,
            )

            drivers.append(
                {
                    "factor": "Behavioural Incidents",
                    "impact": round(float(impact), 2),
                    "type": "risk",
                    "explanation": (
                        f"{data.behavioural_incidents} "
                        "behavioural incidents are recorded."
                    ),
                }
            )

        drivers.sort(
            key=lambda item: item["impact"],
            reverse=True,
        )

        return drivers

    # =========================================================
    # RECOMMENDATION ENGINE
    # =========================================================

    @staticmethod
    def _recommendations(
        data: StudentIntelligenceRequest,
    ) -> List[Dict[str, str]]:

        recommendations: List[Dict[str, str]] = []

        if data.attendance_rate < 75:
            recommendations.append(
                {
                    "title": "Attendance Intervention",
                    "priority": "High",
                    "action": (
                        "Begin attendance monitoring, "
                        "parent outreach and mentor follow-up."
                    ),
                }
            )

        if data.average_test_score < 60:
            recommendations.append(
                {
                    "title": "Academic Support",
                    "priority": "High",
                    "action": (
                        "Provide remedial learning, tutoring "
                        "or personalized study support."
                    ),
                }
            )

        if data.household_income < 25000:
            recommendations.append(
                {
                    "title": "Financial Support Review",
                    "priority": "Medium",
                    "action": (
                        "Check scholarship and welfare-scheme "
                        "eligibility."
                    ),
                }
            )

        if data.distance_to_school > 5:
            recommendations.append(
                {
                    "title": "Transport Assistance",
                    "priority": "Medium",
                    "action": (
                        "Evaluate school transport support "
                        "for the student."
                    ),
                }
            )

        if not data.internet_access:
            recommendations.append(
                {
                    "title": "Digital Access Support",
                    "priority": "Medium",
                    "action": (
                        "Provide device or internet-learning "
                        "support."
                    ),
                }
            )

        if data.behavioural_incidents > 1:
            recommendations.append(
                {
                    "title": "Counselling Support",
                    "priority": "High",
                    "action": (
                        "Assign counselling or mentoring "
                        "support."
                    ),
                }
            )

        if not recommendations:
            recommendations.append(
                {
                    "title": "Routine Monitoring",
                    "priority": "Low",
                    "action": (
                        "Continue normal student monitoring."
                    ),
                }
            )

        return recommendations[:5]

    # =========================================================
    # 1. AI STUDENT DIGITAL TWIN
    # =========================================================

    def digital_twin(
        self,
        data: StudentIntelligenceRequest,
    ) -> Dict[str, Any]:

        prediction = self._predict(
            attendance_rate=data.attendance_rate,
            average_test_score=data.average_test_score,
            household_income=data.household_income,
            distance_to_school=data.distance_to_school,
            internet_access=data.internet_access,
            behavioural_incidents=data.behavioural_incidents,
        )

        # -----------------------------------------------------
        # Learning Stability Score
        # -----------------------------------------------------

        stability = (
            data.attendance_rate * 0.45
            + data.average_test_score * 0.40
            + (8 if data.internet_access else 0)
            - min(
                data.behavioural_incidents * 4,
                16,
            )
            - min(
                data.distance_to_school * 0.6,
                10,
            )
        )

        stability = round(
            self._clamp(stability),
            2,
        )

        return {
            "feature": "AI Student Digital Twin",

            "student": {
                "student_id": data.student_id,
                "student_name": data.student_name,
                "grade": data.grade,
                "school_name": data.school_name,
                "district": data.district,
            },

            "current_risk": prediction,

            "learning_stability_score": stability,

            "live_metrics": {
                "attendance_rate": data.attendance_rate,
                "average_test_score": data.average_test_score,
                "household_income": data.household_income,
                "distance_to_school": data.distance_to_school,
                "internet_access": data.internet_access,
                "behavioural_incidents": (
                    data.behavioural_incidents
                ),
            },

            "risk_drivers": self._risk_drivers(data),

            "recommendations": self._recommendations(data),

            "engine": (
                "VIZHIPPAAN CatBoost Risk Intelligence"
            ),
        }

    # =========================================================
    # 2. STUDENT JOURNEY TIMELINE
    # =========================================================

    def journey_timeline(
        self,
        data: StudentIntelligenceRequest,
    ) -> Dict[str, Any]:

        timeline: List[Dict[str, Any]] = []

        # -----------------------------------------------------
        # Historical snapshots
        # -----------------------------------------------------

        for point in data.history:
            prediction = self._predict(
                attendance_rate=point.attendance_rate,
                average_test_score=point.average_test_score,
                household_income=data.household_income,
                distance_to_school=data.distance_to_school,
                internet_access=data.internet_access,
                behavioural_incidents=(
                    point.behavioural_incidents
                ),
            )

            timeline.append(
                {
                    "period": point.period,
                    "attendance_rate": (
                        point.attendance_rate
                    ),
                    "average_test_score": (
                        point.average_test_score
                    ),
                    "behavioural_incidents": (
                        point.behavioural_incidents
                    ),
                    "risk_probability": (
                        prediction["probability"]
                    ),
                    "risk_level": (
                        prediction["risk_level"]
                    ),
                }
            )

        # -----------------------------------------------------
        # Current snapshot
        # -----------------------------------------------------

        current_prediction = self._predict(
            attendance_rate=data.attendance_rate,
            average_test_score=data.average_test_score,
            household_income=data.household_income,
            distance_to_school=data.distance_to_school,
            internet_access=data.internet_access,
            behavioural_incidents=data.behavioural_incidents,
        )

        timeline.append(
            {
                "period": "Current",
                "attendance_rate": data.attendance_rate,
                "average_test_score": (
                    data.average_test_score
                ),
                "behavioural_incidents": (
                    data.behavioural_incidents
                ),
                "risk_probability": (
                    current_prediction["probability"]
                ),
                "risk_level": (
                    current_prediction["risk_level"]
                ),
            }
        )

        # -----------------------------------------------------
        # Risk trajectory
        # -----------------------------------------------------

        risk_change = 0.0

        if len(timeline) > 1:
            risk_change = round(
                timeline[-1]["risk_probability"]
                - timeline[0]["risk_probability"],
                2,
            )

        if risk_change > 5:
            trajectory = "Worsening"

        elif risk_change < -5:
            trajectory = "Improving"

        else:
            trajectory = "Stable"

        return {
            "feature": "Student Journey Timeline",
            "student_id": data.student_id,
            "timeline": timeline,
            "risk_change": risk_change,
            "trajectory": trajectory,
        }

    # =========================================================
    # 3. RISK EXPLANATION
    # =========================================================

    def risk_explanation(
        self,
        data: StudentIntelligenceRequest,
    ) -> Dict[str, Any]:

        prediction = self._predict(
            attendance_rate=data.attendance_rate,
            average_test_score=data.average_test_score,
            household_income=data.household_income,
            distance_to_school=data.distance_to_school,
            internet_access=data.internet_access,
            behavioural_incidents=data.behavioural_incidents,
        )

        drivers = self._risk_drivers(data)

        risk_factors = [
            factor
            for factor in drivers
            if factor["type"] == "risk"
        ]

        protective_factors = [
            factor
            for factor in drivers
            if factor["type"] == "protective"
        ]

        primary_reason = (
            risk_factors[0]["factor"]
            if risk_factors
            else "No major risk factor"
        )

        return {
            "feature": "Risk Explanation",

            "student_id": data.student_id,

            "prediction": prediction,

            "primary_reason": primary_reason,

            "risk_factors": risk_factors,

            "protective_factors": protective_factors,

            "explanation_method": (
                "CatBoost prediction with "
                "feature-level rule-assisted explanation"
            ),

            "note": (
                "The contribution values represent "
                "rule-based feature severity and are "
                "not SHAP values."
            ),
        }

    # =========================================================
    # 4. EARLY WARNING HORIZON
    # =========================================================

    def early_warning(
        self,
        data: StudentIntelligenceRequest,
    ) -> Dict[str, Any]:

        prediction = self._predict(
            attendance_rate=data.attendance_rate,
            average_test_score=data.average_test_score,
            household_income=data.household_income,
            distance_to_school=data.distance_to_school,
            internet_access=data.internet_access,
            behavioural_incidents=data.behavioural_incidents,
        )

        current_probability = prediction["probability"]

        trend_pressure = 0.0

        history = data.history

        # -----------------------------------------------------
        # Historical trend analysis
        # -----------------------------------------------------

        if len(history) >= 2:
            first = history[0]
            last = history[-1]

            attendance_change = (
                last.attendance_rate
                - first.attendance_rate
            )

            score_change = (
                last.average_test_score
                - first.average_test_score
            )

            incident_change = (
                last.behavioural_incidents
                - first.behavioural_incidents
            )

            # Attendance trend
            if attendance_change < 0:
                trend_pressure += min(
                    12,
                    abs(attendance_change) * 0.5,
                )
            else:
                trend_pressure -= min(
                    8,
                    attendance_change * 0.3,
                )

            # Academic trend
            if score_change < 0:
                trend_pressure += min(
                    10,
                    abs(score_change) * 0.4,
                )
            else:
                trend_pressure -= min(
                    7,
                    score_change * 0.25,
                )

            # Behavioural trend
            trend_pressure += min(
                8,
                max(0, incident_change) * 2,
            )

        # -----------------------------------------------------
        # Fallback when history is unavailable
        # -----------------------------------------------------

        else:
            if data.attendance_rate < 70:
                trend_pressure += 5

            if data.average_test_score < 55:
                trend_pressure += 4

            trend_pressure += min(
                data.behavioural_incidents,
                5,
            )

        # -----------------------------------------------------
        # Socioeconomic pressure
        # -----------------------------------------------------

        if data.household_income < 15000:
            trend_pressure += 2

        if not data.internet_access:
            trend_pressure += 1

        # -----------------------------------------------------
        # Forecast horizons
        # -----------------------------------------------------

        risk_30 = self._clamp(
            current_probability
            + trend_pressure * 0.35
        )

        risk_60 = self._clamp(
            current_probability
            + trend_pressure * 0.60
        )

        risk_90 = self._clamp(
            current_probability
            + trend_pressure
        )

        horizons = [
            {
                "days": 30,
                "probability": round(risk_30, 2),
                "risk_level": (
                    self._risk_level(risk_30)
                ),
            },
            {
                "days": 60,
                "probability": round(risk_60, 2),
                "risk_level": (
                    self._risk_level(risk_60)
                ),
            },
            {
                "days": 90,
                "probability": round(risk_90, 2),
                "risk_level": (
                    self._risk_level(risk_90)
                ),
            },
        ]

        # -----------------------------------------------------
        # Warning message
        # -----------------------------------------------------

        if risk_90 >= 75:
            warning = (
                "Immediate intervention recommended"
            )

        elif risk_90 >= 50:
            warning = (
                "Close monitoring recommended"
            )

        else:
            warning = (
                "Continue routine monitoring"
            )

        return {
            "feature": "Early Warning Horizon",

            "student_id": data.student_id,

            "current_probability": (
                current_probability
            ),

            "current_risk_level": (
                prediction["risk_level"]
            ),

            "horizons": horizons,

            "trend_pressure": round(
                trend_pressure,
                2,
            ),

            "warning": warning,

            "forecast_method": (
                "Scenario projection using current "
                "CatBoost risk plus recent student trend."
            ),
        }


# =============================================================
# SERVICE INSTANCE
# =============================================================

student_intelligence_service = (
    StudentIntelligenceService()
)
