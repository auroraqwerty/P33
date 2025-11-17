from fastapi import APIRouter, HTTPException
from app.services.calculator_service import CalculatorService
from app.models.request_models import GradeRequest
from app.models.response_models import APIResponse

router = APIRouter()
calculator = CalculatorService()

@router.post("/grades", response_model=APIResponse)
async def calculate_grades(request: GradeRequest):
    try:
        result = calculator.calculate_grades(request.grades)
        return APIResponse(
            success=True,
            message="Grades calculated successfully",
            data={"grades": result.dict()}
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))