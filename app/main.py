from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import classes, attendance, grades, time_calculations

app = FastAPI(
    title="Student Management System",
    description="Backend API for mobile student management app",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(classes.router, prefix="/api/v1", tags=["classes"])
app.include_router(attendance.router, prefix="/api/v1", tags=["attendance"])
app.include_router(grades.router, prefix="/api/v1", tags=["grades"])
app.include_router(time_calculations.router, prefix="/api/v1", tags=["time"])

@app.get("/")
async def root():
    return {
        "message": "Student Management System API",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}