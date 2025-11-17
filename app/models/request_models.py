from pydantic import BaseModel, Field
from typing import Dict

class ClassCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

class ClassUpdateRequest(BaseModel):
    new_name: str = Field(..., min_length=1, max_length=100)

class AttendanceRequest(BaseModel):
    total_classes: int = Field(..., ge=1, le=1000)
    missed_classes: int = Field(..., ge=0, le=1000)

class GradeRequest(BaseModel):
    grades: Dict[str, float] = Field(...)

class TimeRequest(BaseModel):
    exit_hour: int = Field(..., ge=0, le=23)
    exit_minute: int = Field(..., ge=0, le=59)