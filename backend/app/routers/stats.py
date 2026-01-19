from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.schemas.schemas import StatisticsResponse, HealthResponse
from app.services.car_service import CarService

router = APIRouter(prefix="/api", tags=["stats"])


@router.get("/statistics", response_model=StatisticsResponse)
def get_statistics(db: Session = Depends(get_db)):
    """Get system statistics"""
    total_cars = CarService.get_total_cars(db)
    available_cars = CarService.count_available_cars(db)
    rented_cars = CarService.count_rented_cars(db)
    average_mileage = CarService.get_average_mileage(db)
    
    return StatisticsResponse(
        total_cars=total_cars,
        available_cars=available_cars,
        rented_cars=rented_cars,
        average_mileage=average_mileage
    )


@router.get("/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow()
    )
