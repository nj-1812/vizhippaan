from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any


class JourneyTimelineService:
    """
    Builds the Student Journey Timeline.

    This service is intentionally independent from FastAPI so that
    timeline-generation logic stays outside the router layer.

    Later this can be connected directly to the real VIZHIPPAAN
    dataset/database.
    """

    def _risk_level(self, score: float) -> str:
        if score >= 0.80:
            return "Critical"
        if score >= 0.60:
            return "High"
        if score >= 0.35:
            return "Medium"
        return "Low"

    def _severity(self, risk_score: float) -> str:
        if risk_score >= 0.80:
            return "critical"
        if risk_score >= 0.60:
            return "high"
        if risk_score >= 0.35:
            return "medium"
        return "low"

    def _event(
        self,
        event_id: str,
        event_type: str,
        title: str,
        description: str,
        timestamp: datetime,
        value: Any = None,
        severity: str = "info",
    ) -> dict[str, Any]:

        return {
            "id": event_id,
            "type": event_type,
            "title": title,
            "description": description,
            "timestamp": timestamp.isoformat(),
            "value": value,
            "severity": severity,
        }

    def build_timeline(
        self,
        student_id: str,
        attendance_rate: float,
        average_test_score: float,
        behavioural_incidents: int,
        household_income: float,
        distance_to_school: float,
        internet_access: bool,
    ) -> dict[str, Any]:

        now = datetime.now(timezone.utc)

        events: list[dict[str, Any]] = []

        # ---------------------------------------------------------
        # Attendance
        # ---------------------------------------------------------

        if attendance_rate < 75:
            attendance_risk = 0.80
            description = (
                f"Attendance has fallen to {attendance_rate:.1f}%. "
                "Immediate attendance intervention is recommended."
            )

        elif attendance_rate < 85:
            attendance_risk = 0.55
            description = (
                f"Attendance is currently {attendance_rate:.1f}%. "
                "The student should be monitored for continued absence."
            )

        else:
            attendance_risk = 0.15
            description = (
                f"Attendance remains stable at {attendance_rate:.1f}%."
            )

        events.append(
            self._event(
                "attendance-1",
                "attendance",
                "Attendance Review",
                description,
                now - timedelta(days=28),
                attendance_rate,
                self._severity(attendance_risk),
            )
        )

        # ---------------------------------------------------------
        # Academic performance
        # ---------------------------------------------------------

        if average_test_score < 40:
            academic_risk = 0.85
            academic_description = (
                f"Average academic score is {average_test_score:.1f}. "
                "Significant academic support may be required."
            )

        elif average_test_score < 60:
            academic_risk = 0.55
            academic_description = (
                f"Average academic score is {average_test_score:.1f}. "
                "Academic performance requires monitoring."
            )

        else:
            academic_risk = 0.15
            academic_description = (
                f"Academic performance remains stable with an "
                f"average score of {average_test_score:.1f}."
            )

        events.append(
            self._event(
                "academic-1",
                "academic",
                "Academic Performance Review",
                academic_description,
                now - timedelta(days=21),
                average_test_score,
                self._severity(academic_risk),
            )
        )

        # ---------------------------------------------------------
        # Behaviour
        # ---------------------------------------------------------

        behaviour_risk = min(1.0, behavioural_incidents / 8)

        events.append(
            self._event(
                "behaviour-1",
                "behaviour",
                "Behavioural Assessment",
                (
                    f"{behavioural_incidents} behavioural incident(s) "
                    "recorded during the current monitoring period."
                ),
                now - timedelta(days=16),
                behavioural_incidents,
                self._severity(behaviour_risk),
            )
        )

        # ---------------------------------------------------------
        # Digital access
        # ---------------------------------------------------------

        digital_risk = 0.65 if not internet_access else 0.10

        events.append(
            self._event(
                "digital-1",
                "digital_access",
                "Digital Access Review",
                (
                    "Student currently has reliable internet access."
                    if internet_access
                    else
                    "Student does not have reliable internet access. "
                    "Digital learning support may be required."
                ),
                now - timedelta(days=12),
                internet_access,
                self._severity(digital_risk),
            )
        )

        # ---------------------------------------------------------
        # Distance / accessibility
        # ---------------------------------------------------------

        distance_risk = min(1.0, distance_to_school / 20)

        events.append(
            self._event(
                "distance-1",
                "accessibility",
                "School Accessibility Review",
                (
                    f"Student travels approximately "
                    f"{distance_to_school:.1f} km to school."
                ),
                now - timedelta(days=9),
                distance_to_school,
                self._severity(distance_risk),
            )
        )

        # ---------------------------------------------------------
        # Socioeconomic condition
        # ---------------------------------------------------------

        if household_income < 100000:
            socioeconomic_risk = 0.75
        elif household_income < 200000:
            socioeconomic_risk = 0.45
        else:
            socioeconomic_risk = 0.15

        events.append(
            self._event(
                "socioeconomic-1",
                "socioeconomic",
                "Socioeconomic Review",
                "Household socioeconomic indicators were reassessed.",
                now - timedelta(days=5),
                household_income,
                self._severity(socioeconomic_risk),
            )
        )

        # ---------------------------------------------------------
        # Overall risk
        # ---------------------------------------------------------

        risk_score = (
            attendance_risk * 0.30
            + academic_risk * 0.25
            + behaviour_risk * 0.15
            + socioeconomic_risk * 0.15
            + digital_risk * 0.10
            + distance_risk * 0.05
        )

        risk_score = max(0.0, min(1.0, risk_score))

        risk_level = self._risk_level(risk_score)

        events.append(
            self._event(
                "risk-1",
                "risk_assessment",
                "Latest Risk Assessment",
                (
                    f"Student is currently classified as "
                    f"{risk_level} Risk."
                ),
                now,
                round(risk_score * 100, 2),
                self._severity(risk_score),
            )
        )

        # Newest event first
        events.sort(
            key=lambda event: event["timestamp"],
            reverse=True,
        )

        return {
            "student_id": student_id,
            "generated_at": now.isoformat(),
            "current_risk": {
                "score": round(risk_score * 100, 2),
                "level": risk_level,
            },
            "summary": {
                "attendance_rate": attendance_rate,
                "average_test_score": average_test_score,
                "behavioural_incidents": behavioural_incidents,
                "distance_to_school": distance_to_school,
                "internet_access": internet_access,
            },
            "event_count": len(events),
            "events": events,
        }


journey_timeline_service = JourneyTimelineService()
