from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.models import Car, CarStatus
from app.schemas.schemas import CarCreate, CarUpdate


class CarService:
    """Service layer for car operations"""

    @staticmethod
    def create_car(db: Session, car: CarCreate) -> Car:
        """Create a new car"""
        db_car = Car(**car.dict())
        db.add(db_car)
        db.commit()
        db.refresh(db_car)
        return db_car

    @staticmethod
    def get_car(db: Session, car_id: int) -> Car:
        """Get car by ID"""
        return db.query(Car).filter(Car.id == car_id).first()

    @staticmethod
    def get_car_by_imma(db: Session, num_imma: str) -> Car:
        """Get car by license plate"""
        return db.query(Car).filter(Car.num_imma == num_imma).first()

    @staticmethod
    def get_all_cars(db: Session, skip: int = 0, limit: int = 100):
        """Get all cars with pagination"""
        return db.query(Car).offset(skip).limit(limit).all()

    @staticmethod
    def update_car(db: Session, car_id: int, car_update: CarUpdate) -> Car:
        """Update car details"""
        db_car = db.query(Car).filter(Car.id == car_id).first()
        if db_car:
            update_data = car_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_car, field, value)
            db.commit()
            db.refresh(db_car)
        return db_car

    @staticmethod
    def delete_car(db: Session, car_id: int) -> bool:
        """Delete a car"""
        db_car = db.query(Car).filter(Car.id == car_id).first()
        if db_car:
            db.delete(db_car)
            db.commit()
            return True
        return False

    @staticmethod
    def get_available_cars(db: Session):
        """Get all available cars"""
        return db.query(Car).filter(Car.etat == CarStatus.AVAILABLE).all()

    @staticmethod
    def get_rented_cars(db: Session):
        """Get all rented cars"""
        return db.query(Car).filter(Car.etat == CarStatus.RENTED).all()

    @staticmethod
    def count_available_cars(db: Session) -> int:
        """Count available cars"""
        return db.query(Car).filter(Car.etat == CarStatus.AVAILABLE).count()

    @staticmethod
    def count_rented_cars(db: Session) -> int:
        """Count rented cars"""
        return db.query(Car).filter(Car.etat == CarStatus.RENTED).count()

    @staticmethod
    def get_average_mileage(db: Session) -> float:
        """Calculate average mileage"""
        result = db.query(func.avg(Car.kilometrage)).scalar()
        return result if result else 0.0

    @staticmethod
    def get_total_cars(db: Session) -> int:
        """Count total cars"""
        return db.query(Car).count()
