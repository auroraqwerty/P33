from fastapi import APIRouter, HTTPException
from app.services.class_service import ClassService
from app.models.request_models import ClassCreateRequest, ClassUpdateRequest
from app.models.response_models import APIResponse

router = APIRouter()
class_service = ClassService()


@router.get("/classes", response_model=APIResponse)
async def get_classes():
    classes = class_service.get_all_classes()
    return APIResponse(
        success=True,
        message="Classes retrieved successfully",
        data={"classes": [cls.dict() for cls in classes]}
    )


@router.post("/classes", response_model=APIResponse)
async def create_class(request: ClassCreateRequest):
    if not request.name.strip():
        raise HTTPException(status_code=400, detail="Class name cannot be empty")

    new_class = class_service.create_class(request.name.strip())
    return APIResponse(
        success=True,
        message="Class created successfully",
        data={"class": new_class.dict()}
    )


@router.put("/classes/{class_id}", response_model=APIResponse)
async def update_class(class_id: int, request: ClassUpdateRequest):
    if not request.new_name.strip():
        raise HTTPException(status_code=400, detail="Class name cannot be empty")

    updated_class = class_service.update_class(class_id, request.new_name.strip())
    if not updated_class:
        raise HTTPException(status_code=404, detail="Class not found")

    return APIResponse(
        success=True,
        message="Class updated successfully",
        data={"class": updated_class.dict()}
    )


@router.delete("/classes/{class_id}", response_model=APIResponse)
async def delete_class(class_id: int):
    if class_service.delete_class(class_id):
        return APIResponse(
            success=True,
            message="Class deleted successfully"
        )
    raise HTTPException(status_code=404, detail="Class not found")