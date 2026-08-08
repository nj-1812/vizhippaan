from datetime import datetime, timezone
from typing import Dict, Any, List

from app.services.model_service import model_service
from app.schemas.digital_twin import (
    StudentTwinRequest,
)


class DigitalTwinService:

    # =========================================================
    # RISK LEVEL HELPER
    # =========================================================

    @staticmethod
    def risk_level(probability: float) -> str:
        """
        probability must be between 0 and 100
        """

        if probability < 25:
            return "Low"

        if probability < 50:
            return "Medium"

        if probability < 75:
            return "High"

        return "Critical"

    # =========================================================
    # LEARNING STABILITY SCORE
    # =========================================================

    @staticmethod
    def calculate_learning_stability(
        data: StudentTwinRequest,
    ) -> float:

        attendance_component = (
            data.attendance_rate * 0.40
        )

        academic_component = (
            data.average_test_score * 0.40
        )

        behaviour_penalty = min(
            data.behavioural_incidents * 5,
            20,
        )

        digital_component = (
            10 if data.internet_access else 0
        )

        commute_penalty = min(
            data.distance_to_school * 0.5,
            10,
        )

        score = (
            attendance_component
            + academic_component
            + digital_component
            - behaviour_penalty
            - commute_penalty
        )

        return round(
            max(0, min(100, score)),
            2,
        )

    # =========================================================
    # RISK DRIVERS
    # =========================================================

    @staticmethod
    def calculate_risk_drivers(
        data: StudentTwinRequest,
    ) -> List[Dict[str, Any]]:

        drivers = []

        # -----------------------------------------------------
        # ATTENDANCE
        # -----------------------------------------------------

        if data.attendance_rate < 75:

            impact = min(
                100,
                (75 - data.attendance_rate) * 2,
            )

            drivers.append({
                "factor": "Low Attendance",
                "impact": round(impact, 2),
                "severity": (
                    "Critical"
                    if data.attendance_rate < 50
                    else "High"
                ),
                "direction": "increases_risk",
                "explanation":
                    f"Attendance is only "
                    f"{data.attendance_rate:.1f}%.",
            })

        # -----------------------------------------------------
        # ACADEMICS
        # -----------------------------------------------------

        if data.average_test_score < 60:

            impact = min(
                100,
                (60 - data.average_test_score) * 1.5,
            )

            drivers.append({
                "factor":
                    "Low Academic Performance",

                "impact":
                    round(impact, 2),

                "severity":
                    (
                        "High"
                        if data.average_test_score < 40
                        else "Medium"
                    ),

                "direction":
                    "increases_risk",

                "explanation":
                    f"Average test score is "
                    f"{data.average_test_score:.1f}%.",
            })

        # -----------------------------------------------------
        # HOUSEHOLD INCOME
        # -----------------------------------------------------

        if data.household_income < 25000:

            income_gap = (
                25000
                - data.household_income
            )

            impact = min(
                100,
                income_gap / 300,
            )

            drivers.append({
                "factor":
                    "Economic Vulnerability",

                "impact":
                    round(impact, 2),

                "severity":
                    (
                        "High"
                        if data.household_income < 15000
                        else "Medium"
                    ),

                "direction":
                    "increases_risk",

                "explanation":
                    "Household income may create "
                    "financial barriers to continued education.",
            })

        # -----------------------------------------------------
        # SCHOOL DISTANCE
        # -----------------------------------------------------

        if data.distance_to_school > 5:

            impact = min(
                100,
                (
                    data.distance_to_school - 5
                ) * 5,
            )

            drivers.append({
                "factor":
                    "Long Distance To School",

                "impact":
                    round(impact, 2),

                "severity":
                    (
                        "High"
                        if data.distance_to_school > 12
                        else "Medium"
                    ),

                "direction":
                    "increases_risk",

                "explanation":
                    f"Student travels "
                    f"{data.distance_to_school:.1f} km "
                    f"to school.",
            })

        # -----------------------------------------------------
        # INTERNET
        # -----------------------------------------------------

        if not data.internet_access:

            drivers.append({
                "factor":
                    "No Internet Access",

                "impact":
                    25.0,

                "severity":
                    "Medium",

                "direction":
                    "increases_risk",

                "explanation":
                    "The student has limited digital "
                    "learning access.",
            })

        # -----------------------------------------------------
        # BEHAVIOURAL INCIDENTS
        # -----------------------------------------------------

        if data.behavioural_incidents > 0:

            impact = min(
                100,
                data.behavioural_incidents * 12,
            )

            drivers.append({
                "factor":
                    "Behavioural Incidents",

                "impact":
                    round(impact, 2),

                "severity":
                    (
                        "High"
                        if data.behavioural_incidents >= 4
                        else "Medium"
                    ),

                "direction":
                    "increases_risk",

                "explanation":
                    f"{data.behavioural_incidents} "
                    f"behavioural incidents recorded.",
            })

        # Highest impact first

        drivers.sort(
            key=lambda x: x["impact"],
            reverse=True,
        )

        return drivers[:6]

    # =========================================================
    # FUTURE RISK PROJECTION
    # =========================================================

    def build_horizons(
        self,
        current_probability: float,
        data: StudentTwinRequest,
    ) -> List[Dict[str, Any]]:

        trend_adjustment = 0.0

        # Attendance worsening

        if (
            data.previous_attendance_rate
            is not None
        ):
            attendance_change = (
                data.attendance_rate
                - data.previous_attendance_rate
            )

            if attendance_change < 0:
                trend_adjustment += min(
                    10,
                    abs(attendance_change) * 0.5,
                )

            else:
                trend_adjustment -= min(
                    7,
                    attendance_change * 0.3,
                )

        # Academic worsening

        if (
            data.previous_test_score
            is not None
        ):
            score_change = (
                data.average_test_score
                - data.previous_test_score
            )

            if score_change < 0:
                trend_adjustment += min(
                    10,
                    abs(score_change) * 0.4,
                )

            else:
                trend_adjustment -= min(
                    7,
                    score_change * 0.25,
                )

        behaviour_effect = min(
            data.behavioural_incidents * 1.5,
            8,
        )

        base_growth = (
            trend_adjustment
            + behaviour_effect
        )

        day30 = max(
            0,
            min(
                100,
                current_probability
                + base_growth * 0.35,
            ),
        )

        day90 = max(
            0,
            min(
                100,
                current_probability
                + base_growth * 0.75,
            ),
        )

        end_year = max(
            0,
            min(
                100,
                current_probability
                + base_growth,
            ),
        )

        return [
            {
                "horizon":
                    "30 Days",

                "probability":
                    round(day30, 2),

                "risk_level":
                    self.risk_level(day30),
            },
            {
                "horizon":
                    "90 Days",

                "probability":
                    round(day90, 2),

                "risk_level":
                    self.risk_level(day90),
            },
            {
                "horizon":
                    "End of Year",

                "probability":
                    round(end_year, 2),

                "risk_level":
                    self.risk_level(end_year),
            },
        ]

    # =========================================================
    # RECOMMENDATION ENGINE
    # =========================================================

    @staticmethod
    def recommendations(
        data: StudentTwinRequest,
    ) -> List[Dict[str, str]]:

        actions = []

        if data.attendance_rate < 75:

            actions.append({
                "title":
                    "Attendance Intervention",

                "priority":
                    "High",

                "reason":
                    "Attendance is below the recommended "
                    "stability threshold.",
            })

        if data.average_test_score < 60:

            actions.append({
                "title":
                    "Academic Support",

                "priority":
                    "High",

                "reason":
                    "Student may benefit from remedial "
                    "classes or tutoring.",
            })

        if data.household_income < 25000:

            actions.append({
                "title":
                    "Scholarship / Welfare Assessment",

                "priority":
                    "Medium",

                "reason":
                    "Financial vulnerability may be "
                    "affecting educational continuity.",
            })

        if data.distance_to_school > 5:

            actions.append({
                "title":
                    "Transport Support",

                "priority":
                    "Medium",

                "reason":
                    "Long commute distance may contribute "
                    "to irregular attendance.",
            })

        if not data.internet_access:

            actions.append({
                "title":
                    "Digital Access Support",

                "priority":
                    "Medium",

                "reason":
                    "Student lacks reliable digital "
                    "learning access.",
            })

        if data.behavioural_incidents > 1:

            actions.append({
                "title":
                    "Counselling Support",

                "priority":
                    "High",

                "reason":
                    "Behavioural incidents indicate a need "
                    "for mentoring or counselling.",
            })

        if not actions:

            actions.append({
                "title":
                    "Continue Routine Monitoring",

                "priority":
                    "Low",

                "reason":
                    "No major intervention trigger "
                    "is currently detected.",
            })

        return actions[:5]

    # =========================================================
    # MAIN DIGITAL TWIN
    # =========================================================

    def generate(
        self,
        data: StudentTwinRequest,
    ) -> Dict[str, Any]:

        # -----------------------------------------------------
        # Send exactly the fields expected by your CatBoost
        # model prediction service
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # Handle the response format already used in your API
        # -----------------------------------------------------

        probability = float(
            prediction.get(
                "dropout_probability",
                0,
            )
        )

        # In case model service returns 0.62 instead of 62

        if probability <= 1:
            probability *= 100

        probability = round(
            max(
                0,
                min(100, probability)
            ),
            2,
        )

        predicted_risk = prediction.get(
            "predicted_risk"
        ) or self.risk_level(
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
                min(100, confidence)
            ),
            2,
        )

        # -----------------------------------------------------
        # Digital Twin Intelligence
        # -----------------------------------------------------

        stability = (
            self.calculate_learning_stability(
                data
            )
        )

        drivers = (
            self.calculate_risk_drivers(
                data
            )
        )

        horizons = (
            self.build_horizons(
                probability,
                data,
            )
        )

        recommendations = (
            self.recommendations(
                data
            )
        )

        return {
            "student_id":
                data.student_id,

            "student_name":
                data.student_name
                or "Student",

            "grade":
                data.grade,

            "school_name":
                data.school_name,

            "district":
                data.district,

            "current_risk": {
                "probability":
                    probability,

                "risk_level":
                    predicted_risk,
            },

            "learning_stability_score":
                stability,

            "confidence_score":
                confidence,

            "horizons":
                horizons,

            "risk_drivers":
                drivers,

            "recommendations":
                recommendations,

            "live_metrics": {
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
            },

            "model_status":
                "CatBoost model active",

            "projection_method":
                (
                    "Current risk uses trained CatBoost model. "
                    "Future horizons are scenario projections "
                    "based on current risk and recent trend."
                ),

            "generated_at":
                datetime.now(
                    timezone.utc
                ).isoformat(),
        }


digital_twin_service = (
    DigitalTwinService()
)
