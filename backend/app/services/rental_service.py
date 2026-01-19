from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from app.models.models import Rental, Car, CarStatus
from app.schemas.schemas import RentalCreate, RentalReturn


class RentalService:
    """Service layer for rental operations"""

    @staticmethod
    def create_rental(db: Session, rental: RentalCreate) -> Rental:
        """Create a new rental"""
        # Check if car exists and is available
        car = db.query(Car).filter(Car.id == rental.car_id).first()
        if not car:
            return None
        if car.etat != CarStatus.AVAILABLE:
            return None

        # Create rental and update car status
        db_rental = Rental(**rental.dict())
        db.add(db_rental)
        car.etat = CarStatus.RENTED
        db.commit()
        db.refresh(db_rental)
        return db_rental

    @staticmethod
    def get_rental(db: Session, rental_id: int) -> Rental:
        """Get rental by ID"""
        return db.query(Rental).filter(Rental.id == rental_id).first()

    @staticmethod
    def get_all_rentals(db: Session, skip: int = 0, limit: int = 100):
        """Get all rentals with pagination"""
        return db.query(Rental).offset(skip).limit(limit).all()

    @staticmethod
    def get_active_rentals(db: Session):
        """Get active rentals (not returned)"""
        return db.query(Rental).filter(Rental.date_retour.is_(None)).all()

    @staticmethod
    def get_rental_history(db: Session, customer_id: int):
        """Get rental history for a customer"""
        return db.query(Rental).filter(Rental.customer_id == customer_id).all()

    @staticmethod
    def get_car_rental_history(db: Session, car_id: int):
        """Get rental history for a car"""
        return db.query(Rental).filter(Rental.car_id == car_id).all()

    @staticmethod
    def return_rental(db: Session, rental_id: int, return_data: RentalReturn) -> Rental:
        """Return a rented car"""
        db_rental = db.query(Rental).filter(Rental.id == rental_id).first()
        if not db_rental:
            return None

        # Update rental with return information
        db_rental.date_retour = return_data.date_retour or datetime.utcnow()
        db_rental.date_fin = datetime.utcnow()

        # Update car status back to available
        car = db.query(Car).filter(Car.id == db_rental.car_id).first()
        if car:
            car.etat = CarStatus.AVAILABLE

        db.commit()
        db.refresh(db_rental)
        return db_rental

    @staticmethod
    def delete_rental(db: Session, rental_id: int) -> bool:
        """Delete a rental"""
        db_rental = db.query(Rental).filter(Rental.id == rental_id).first()
        if db_rental:
            db.delete(db_rental)
            db.commit()
            return True
        return False

    @staticmethod
    def is_car_available(db: Session, car_id: int) -> bool:
        """Check if car is available"""
        car = db.query(Car).filter(Car.id == car_id).first()
        return car and car.etat == CarStatus.AVAILABLE

    @staticmethod
    def count_active_rentals(db: Session) -> int:
        """Count active rentals"""
        return db.query(Rental).filter(Rental.date_retour.is_(None)).count()

    @staticmethod
    def get_total_rentals(db: Session) -> int:
        """Count total rentals"""
        return db.query(Rental).count()
