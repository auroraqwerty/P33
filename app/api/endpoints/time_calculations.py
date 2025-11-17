from fastapi import APIRouter, HTTPException
from app.services.calculator_service import CalculatorService
from app.models.request_models import TimeRequest
from app.models.response_models import APIResponse

router = APIRouter()
calculator = CalculatorService()

@router.post("/time-until-exit", response_model=APIResponse)
async def calculate_time_until_exit(request: TimeRequest):
    try:
        result = calculator.calculate_time_until_exit(
            request.exit_hour,
            request.exit_minute
        )
        return APIResponse(
            success=True,
            message="Time calculated successfully",
            data={"time_until_exit": result.dict()}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))