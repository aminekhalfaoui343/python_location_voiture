from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import CarCreate, CarResponse, CarUpdate
from app.services.car_service import CarService

router = APIRouter(prefix="/api/cars", tags=["cars"])


@router.post("/", response_model=CarResponse, status_code=201)
def create_car(car: CarCreate, db: Session = Depends(get_db)):
    """Create a new car"""
    # Check if car with same license plate exists
    existing_car = CarService.get_car_by_imma(db, car.num_imma)
    if existing_car:
        raise HTTPException(status_code=400, detail="Car with this license plate already exists")

    return CarService.create_car(db, car)


@router.get("/{car_id}", response_model=CarResponse)
def get_car(car_id: int, db: Session = Depends(get_db)):
    """Get car by ID"""
    car = CarService.get_car(db, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car


@router.get("/", response_model=list[CarResponse])
def get_all_cars(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    """Get all cars"""
    return CarService.get_all_cars(db, skip, limit)


@router.put("/{car_id}", response_model=CarResponse)
def update_car(car_id: int, car: CarUpdate, db: Session = Depends(get_db)):
    """Update car details"""
    db_car = CarService.get_car(db, car_id)
    if not db_car:
        raise HTTPException(status_code=404, detail="Car not found")
    
    return CarService.update_car(db, car_id, car)


@router.delete("/{car_id}", status_code=204)
def delete_car(car_id: int, db: Session = Depends(get_db)):
    """Delete a car"""
    success = CarService.delete_car(db, car_id)
    if not success:
        raise HTTPException(status_code=404, detail="Car not found")
    return None


@router.get("/search/available", response_model=list[CarResponse])
def get_available_cars(db: Session = Depends(get_db)):
    """Get all available cars"""
    return CarService.get_available_cars(db)


@router.get("/search/rented", response_model=list[CarResponse])
def get_rented_cars(db: Session = Depends(get_db)):
    """Get all rented cars"""
    return CarService.get_rented_cars(db)
