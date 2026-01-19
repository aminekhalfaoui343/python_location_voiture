from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import RentalCreate, RentalResponse, RentalReturn, RentalDetail
from app.services.rental_service import RentalService

router = APIRouter(prefix="/api/rentals", tags=["rentals"])


@router.post("/", response_model=RentalResponse, status_code=201)
def create_rental(rental: RentalCreate, db: Session = Depends(get_db)):
    """Create a new rental (rent a car to a customer)"""
    # Verify car exists and is available
    from app.services.car_service import CarService
    car = CarService.get_car(db, rental.car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    
    # Verify customer exists
    from app.services.customer_service import CustomerService
    customer = CustomerService.get_customer(db, rental.customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Check if car is available
    if not RentalService.is_car_available(db, rental.car_id):
        raise HTTPException(status_code=400, detail="Car is not available for rental")
    
    db_rental = RentalService.create_rental(db, rental)
    if not db_rental:
        raise HTTPException(status_code=400, detail="Failed to create rental")
    
    return db_rental


@router.get("/{rental_id}", response_model=RentalDetail)
def get_rental(rental_id: int, db: Session = Depends(get_db)):
    """Get rental details by ID"""
    rental = RentalService.get_rental(db, rental_id)
    if not rental:
        raise HTTPException(status_code=404, detail="Rental not found")
    return rental


@router.get("/", response_model=list[RentalResponse])
def get_all_rentals(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    """Get all rentals"""
    return RentalService.get_all_rentals(db, skip, limit)


@router.post("/{rental_id}/return", response_model=RentalResponse)
def return_rental(rental_id: int, return_data: RentalReturn, db: Session = Depends(get_db)):
    """Return a rented car"""
    rental = RentalService.get_rental(db, rental_id)
    if not rental:
        raise HTTPException(status_code=404, detail="Rental not found")
    
    if rental.date_retour is not None:
        raise HTTPException(status_code=400, detail="Car has already been returned")
    
    return RentalService.return_rental(db, rental_id, return_data)


@router.delete("/{rental_id}", status_code=204)
def delete_rental(rental_id: int, db: Session = Depends(get_db)):
    """Delete a rental record"""
    success = RentalService.delete_rental(db, rental_id)
    if not success:
        raise HTTPException(status_code=404, detail="Rental not found")
    return None


@router.get("/search/active", response_model=list[RentalResponse])
def get_active_rentals(db: Session = Depends(get_db)):
    """Get active rentals (not yet returned)"""
    return RentalService.get_active_rentals(db)


@router.get("/search/customer/{customer_id}", response_model=list[RentalResponse])
def get_customer_rentals(customer_id: int, db: Session = Depends(get_db)):
    """Get rental history for a customer"""
    from app.services.customer_service import CustomerService
    customer = CustomerService.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return RentalService.get_rental_history(db, customer_id)


@router.get("/search/car/{car_id}", response_model=list[RentalResponse])
def get_car_rentals(car_id: int, db: Session = Depends(get_db)):
    """Get rental history for a car"""
    from app.services.car_service import CarService
    car = CarService.get_car(db, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    
    return RentalService.get_car_rental_history(db, car_id)
