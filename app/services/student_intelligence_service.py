from typing import Any, Dict, List

from app.schemas.student_intelligence import (
    HistoryPoint,
    StudentIntelligenceRequest,
)

from app.services.model_service import model_service


class StudentIntelligenceService:

    # =========================================================
    # COMMON HELPERS
    # =========================================================

    @staticmethod
    def _clamp(
        value: float,
        minimum: float = 0,
        maximum: float = 100,
    ) -> float:
        return max(
            minimum,
            min(maximum, value),
        )

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

    # =========================================================
    # CATBOOST PREDICTION
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
            "attendance_rate":
                attendance_rate,

            "average_test_score":
                average_test_score,

            "household_income":
                household_income,

            "distance_to_school":
                distance_to_school,

            "internet_access":
                internet_access,

            "behavioural_incidents":
                behavioural_incidents,
        }

        result = model_service.predict(
            payload
        )

        probability = float(
            result.get(
                "dropout_probability",
                result.get(
                    "risk_probability",
                    0,
                ),
            )
        )

        if probability <= 1:
            probability *= 100

        probability = round(
            self._clamp(
                probability
            ),
            2,
        )

        risk_level = (
            result.get(
                "predicted_risk"
            )
            or result.get(
                "risk_level"
            )
            or self._risk_level(
                probability
            )
        )

        confidence = float(
            result.get(
                "confidence_score",
                0,
            )
        )

        if confidence <= 1:
            confidence *= 100

        confidence = round(
            self._clamp(
                confidence
            ),
            2,
        )

        return {
            "probability":
                probability,

            "risk_level":
                risk_level,

            "confidence":
                confidence,

            "raw_prediction":
                result,
        }

    # =========================================================
    # RISK DRIVER ENGINE
    # =========================================================

    def _risk_drivers(
        self,
        data: StudentIntelligenceRequest,
    ) -> List[Dict[str, Any]]:

        drivers = []

        if data.attendance_rate < 75:

            impact = self._clamp(
                (
                    75
                    - data.attendance_rate
                )
                * 2
            )

            drivers.append({
                "factor":
                    "Low Attendance",

                "impact":
                    round(
                        impact,
                        2,
                    ),

                "type":
                    "risk",

                "explanation":
                    (
                        f"Attendance is "
                        f"{data.attendance_rate:.1f}%, "
                        "below the preferred 75% threshold."
                    ),
            })

        else:

            drivers.append({
                "factor":
                    "Stable Attendance",

                "impact":
                    round(
                        min(
                            30,
                            (
                                data.attendance_rate
                                - 75
                            )
                            * 1.2,
                        ),
                        2,
                    ),

                "type":
                    "protective",

                "explanation":
                    "Attendance currently supports continued engagement.",
            })

        if (
            data.average_test_score
            < 60
        ):

            drivers.append({
                "factor":
                    "Low Academic Performance",

                "impact":
                    round(
                        self._clamp(
                            (
                                60
                                - data.average_test_score
                            )
                            * 1.5
                        ),
                        2,
                    ),

                "type":
                    "risk",

                "explanation":
                    (
                        f"Average academic score is "
                        f"{data.average_test_score:.1f}%."
                    ),
            })

        else:

            drivers.append({
                "factor":
                    "Academic Stability",

                "impact":
                    round(
                        min(
                            30,
                            (
                                data.average_test_score
                                - 60
                            ),
                        ),
                        2,
                    ),

                "type":
                    "protective",

                "explanation":
                    "Academic performance is currently stable.",
            })

        if (
            data.household_income
            < 25000
        ):

            drivers.append({
                "factor":
                    "Economic Vulnerability",

                "impact":
                    round(
                        self._clamp(
                            (
                                25000
                                - data.household_income
                            )
                            / 250
                        ),
                        2,
                    ),

                "type":
                    "risk",

                "explanation":
                    "Household income may create financial barriers.",
            })

        if (
            data.distance_to_school
            > 5
        ):

            drivers.append({
                "factor":
                    "Travel Distance",

                "impact":
                    round(
                        self._clamp(
                            (
                                data.distance_to_school
                                - 5
                            )
                            * 5
                        ),
                        2,
                    ),

                "type":
                    "risk",

                "explanation":
                    (
                        f"The student travels "
                        f"{data.distance_to_school:.1f} km "
                        "to school."
                    ),
            })

        if not data.internet_access:

            drivers.append({
                "factor":
                    "No Internet Access",

                "impact":
                    25,

                "type":
                    "risk",

                "explanation":
                    "Reliable digital learning access is unavailable.",
            })

        if (
            data.behavioural_incidents
            > 0
        ):

            drivers.append({
                "factor":
                    "Behavioural Incidents",

                "impact":
                    min(
                        100,
                        data.behavioural_incidents
                        * 12,
                    ),

                "type":
                    "risk",

                "explanation":
                    (
                        f"{data.behavioural_incidents} "
                        "behavioural incidents are recorded."
                    ),
            })

        drivers.sort(
            key=lambda item:
                item["impact"],
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

        recommendations = []

        if data.attendance_rate < 75:

            recommendations.append({
                "title":
                    "Attendance Intervention",

                "priority":
                    "High",

                "action":
                    (
                        "Begin attendance monitoring, "
                        "parent outreach and mentor follow-up."
                    ),
            })

        if (
            data.average_test_score
            < 60
        ):

            recommendations.append({
                "title":
                    "Academic Support",

                "priority":
                    "High",

                "action":
                    (
                        "Provide remedial learning, "
                        "tutoring or personalized study support."
                    ),
            })

        if (
            data.household_income
            < 25000
        ):

            recommendations.append({
                "title":
                    "Financial Support Review",

                "priority":
                    "Medium",

                "action":
                    (
                        "Check scholarship and "
                        "welfare-scheme eligibility."
                    ),
            })

        if (
            data.distance_to_school
            > 5
        ):

            recommendations.append({
                "title":
                    "Transport Assistance",

                "priority":
                    "Medium",

                "action":
                    "Evaluate school transport support.",
            })

        if not data.internet_access:

            recommendations.append({
                "title":
                    "Digital Access Support",

                "priority":
                    "Medium",

                "action":
                    "Provide device or internet-learning support.",
            })

        if (
            data.behavioural_incidents
            > 1
        ):

            recommendations.append({
                "title":
                    "Counselling Support",

                "priority":
                    "High",

                "action":
                    "Assign counselling or mentoring support.",
            })

        if not recommendations:

            recommendations.append({
                "title":
                    "Routine Monitoring",

                "priority":
                    "Low",

                "action":
                    "Continue normal student monitoring.",
            })

        return recommendations[:5]

    # =========================================================
    # 1. AI STUDENT DIGITAL TWIN
    # =========================================================

    def digital_twin(
        self,
        data: StudentIntelligenceRequest,
    ) -> Dict[str, Any]:

        prediction = self._predict(
            data.attendance_rate,
            data.average_test_score,
            data.household_income,
            data.distance_to_school,
            data.internet_access,
            data.behavioural_incidents,
        )

        stability = (
            data.attendance_rate
            * 0.45
            + data.average_test_score
            * 0.40
            + (
                8
                if data.internet_access
                else 0
            )
            - min(
                data.behavioural_incidents
                * 4,
                16,
            )
            - min(
                data.distance_to_school
                * 0.6,
                10,
            )
        )

        stability = round(
            self._clamp(
                stability
            ),
            2,
        )

        return {
            "feature":
                "AI Student Digital Twin",

            "student": {
                "student_id":
                    data.student_id,

                "student_name":
                    data.student_name,

                "grade":
                    data.grade,

                "school_name":
                    data.school_name,

                "district":
                    data.district,
            },

            "current_risk":
                prediction,

            "learning_stability_score":
                stability,

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

            "risk_drivers":
                self._risk_drivers(
                    data
                ),

            "recommendations":
                self._recommendations(
                    data
                ),

            "engine":
                "VIZHIPPAAN CatBoost Risk Intelligence",
        }

    # =========================================================
    # 2. STUDENT JOURNEY TIMELINE
    # =========================================================

    def journey_timeline(
        self,
        data: StudentIntelligenceRequest,
    ) -> Dict[str, Any]:

        timeline = []

        for point in data.history:

            prediction = self._predict(
                point.attendance_rate,
                point.average_test_score,
                data.household_income,
                data.distance_to_school,
                data.internet_access,
                point.behavioural_incidents,
            )

            timeline.append({
                "period":
                    point.period,

                "attendance_rate":
                    point.attendance_rate,

                "average_test_score":
                    point.average_test_score,

                "behavioural_incidents":
                    point.behavioural_incidents,

                "risk_probability":
                    prediction[
                        "probability"
                    ],

                "risk_level":
                    prediction[
                        "risk_level"
                    ],
            })

        current_prediction = (
            self._predict(
                data.attendance_rate,
                data.average_test_score,
                data.household_income,
                data.distance_to_school,
                data.internet_access,
                data.behavioural_incidents,
            )
        )

        timeline.append({
            "period":
                "Current",

            "attendance_rate":
                data.attendance_rate,

            "average_test_score":
                data.average_test_score,

            "behavioural_incidents":
                data.behavioural_incidents,

            "risk_probability":
                current_prediction[
                    "probability"
                ],

            "risk_level":
                current_prediction[
                    "risk_level"
                ],
        })

        risk_change = 0

        if len(timeline) > 1:

            risk_change = round(
                timeline[-1][
                    "risk_probability"
                ]
                - timeline[0][
                    "risk_probability"
                ],
                2,
            )

        return {
            "feature":
                "Student Journey Timeline",

            "student_id":
                data.student_id,

            "timeline":
                timeline,

            "risk_change":
                risk_change,

            "trajectory":
                (
                    "Worsening"
                    if risk_change > 5
                    else
                    "Improving"
                    if risk_change < -5
                    else
                    "Stable"
                ),
        }

    # =========================================================
    # 3. RISK EXPLANATION
    # =========================================================

    def risk_explanation(
        self,
        data: StudentIntelligenceRequest,
    ) -> Dict[str, Any]:

        prediction = self._predict(
            data.attendance_rate,
            data.average_test_score,
            data.household_income,
            data.distance_to_school,
            data.internet_access,
            data.behavioural_incidents,
        )

        drivers = self._risk_drivers(
            data
        )

        risk_factors = [
            factor
            for factor in drivers
            if factor["type"] == "risk"
        ]

        protective_factors = [
            factor
            for factor in drivers
            if factor["type"]
            == "protective"
        ]

        top_reason = (
            risk_factors[0][
                "factor"
            ]
            if risk_factors
            else
            "No major risk factor"
        )

        return {
            "feature":
                "Risk Explanation",

            "student_id":
                data.student_id,

            "prediction":
                prediction,

            "primary_reason":
                top_reason,

            "risk_factors":
                risk_factors,

            "protective_factors":
                protective_factors,

            "explanation_method":
                (
                    "CatBoost prediction with "
                    "feature-level rule-assisted explanation"
                ),

            "note":
                (
                    "These contribution values describe "
                    "feature severity around the prediction; "
                    "they are not SHAP values."
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
            data.attendance_rate,
            data.average_test_score,
            data.household_income,
            data.distance_to_school,
            data.internet_access,
            data.behavioural_incidents,
        )

        current_probability = (
            prediction[
                "probability"
            ]
        )

        trend_pressure = 0.0

        history = data.history

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

            if attendance_change < 0:

                trend_pressure += min(
                    12,
                    abs(
                        attendance_change
                    )
                    * 0.5,
                )

            else:

                trend_pressure -= min(
                    8,
                    attendance_change
                    * 0.3,
                )

            if score_change < 0:

                trend_pressure += min(
                    10,
                    abs(
                        score_change
                    )
                    * 0.4,
                )

            else:

                trend_pressure -= min(
                    7,
                    score_change
                    * 0.25,
                )

            trend_pressure += min(
                8,
                max(
                    0,
                    incident_change
                )
                * 2,
            )

        else:

            if (
                data.attendance_rate
                < 70
            ):
                trend_pressure += 5

            if (
                data.average_test_score
                < 55
            ):
                trend_pressure += 4

            trend_pressure += min(
                data.behavioural_incidents,
                5,
            )

        if (
            data.household_income
            < 15000
        ):
            trend_pressure += 2

        if not data.internet_access:
            trend_pressure += 1

        risk_30 = self._clamp(
            current_probability
            + trend_pressure
            * 0.35
        )

        risk_60 = self._clamp(
            current_probability
            + trend_pressure
            * 0.60
        )

        risk_90 = self._clamp(
            current_probability
            + trend_pressure
        )

        horizons = [
            {
                "days":
                    30,

                "probability":
                    round(
                        risk_30,
                        2,
                    ),

                "risk_level":
                    self._risk_level(
                        risk_30
                    ),
            },

            {
                "days":
                    60,

                "probability":
                    round(
                        risk_60,
                        2,
                    ),

                "risk_level":
                    self._risk_level(
                        risk_60
                    ),
            },

            {
                "days":
                    90,

                "probability":
                    round(
                        risk_90,
                        2,
                    ),

                "risk_level":
                    self._risk_level(
                        risk_90
                    ),
            },
        ]

        return {
            "feature":
                "Early Warning Horizon",

            "student_id":
                data.student_id,

            "current_probability":
                current_probability,

            "current_risk_level":
                prediction[
                    "risk_level"
                ],

            "horizons":
                horizons,

            "trend_pressure":
                round(
                    trend_pressure,
                    2,
                ),

            "warning":
                (
                    "Immediate intervention recommended"
                    if risk_90 >= 75
                    else
                    "Close monitoring recommended"
                    if risk_90 >= 50
                    else
                    "Continue routine monitoring"
                ),

            "forecast_method":
                (
                    "Scenario projection using current "
                    "CatBoost risk plus recent student trend."
                ),
        }


student_intelligence_service = (
    StudentIntelligenceService()
)
