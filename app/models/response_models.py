from pydantic import BaseModel
from typing import Dict, Any, Optional, List

class ClassModel(BaseModel):
    id: int
    name: str

class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None

class AttendanceResponse(BaseModel):
    attended: int
    missed: int
    total: int
    percentage: float

class GradesResponse(BaseModel):
    average: float
    subject_count: int
    grades: Dict[str, float]

class TimeResponse(BaseModel):
    hours: int
    minutes: int
    seconds: int
    total_seconds: int