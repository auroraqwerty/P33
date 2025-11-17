from fastapi import APIRouter, HTTPException
from app.services.calculator_service import CalculatorService
from app.models.request_models import AttendanceRequest
from app.models.response_models import APIResponse

router = APIRouter()
calculator = CalculatorService()

@router.post("/attendance", response_model=APIResponse)
async def calculate_attendance(request: AttendanceRequest):
    try:
        result = calculator.calculate_attendance(
            request.total_classes,
            request.missed_classes
        )
        return APIResponse(
            success=True,
            message="Attendance calculated successfully",
            data={"attendance": result.dict()}
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))