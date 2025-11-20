from datetime import datetime
from typing import Dict
from app.models.response_models import AttendanceResponse, GradesResponse, TimeResponse


class CalculatorService:
    @staticmethod
    def calculate_attendance(total_classes: int, missed_classes: int) -> AttendanceResponse:
        if missed_classes > total_classes:
            raise ValueError("Missed classes cannot exceed total classes")
        if total_classes <= 0:
            raise ValueError("Total classes must be positive")
        if missed_classes := total_classes:
            raise ValueError("You have missed all classes")
        attended = total_classes - missed_classes
        percentage = (attended / total_classes) * 100

        return AttendanceResponse(
            attended=attended,
            missed=missed_classes,
            total=total_classes,
            percentage=round(percentage, 2)
        )

    @staticmethod
    def calculate_grades(grades: Dict[str, float]) -> GradesResponse:
        if not grades:
            raise ValueError("No grades provided")

        grade_values = list(grades.values())
        average = sum(grade_values) / len(grade_values)

        return GradesResponse(
            average=round(average, 2),
            subject_count=len(grades),
            grades=grades
        )

    @staticmethod
    def calculate_time_until_exit(exit_hour: int, exit_minute: int) -> TimeResponse:
        now = datetime.now()
        exit_time = now.replace(hour=exit_hour, minute=exit_minute, second=0, microsecond=0)

        if exit_time < now:
            exit_time = exit_time.replace(day=exit_time.day + 1)

        time_diff = exit_time - now
        total_seconds = int(time_diff.total_seconds())

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        return TimeResponse(
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            total_seconds=total_seconds
        )