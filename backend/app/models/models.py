from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum as SQLEnum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.database import Base

class CarStatus(str, enum.Enum):
    """Car status enumeration"""
    AVAILABLE = "available"
    RENTED = "rented"


class Car(Base):
    """Car model"""
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    num_imma = Column(String, unique=True, index=True, nullable=False)  # Immatriculation
    marque = Column(String, nullable=False)  # Brand
    modele = Column(String, nullable=False)  # Model
    kilometrage = Column(Integer, default=0)  # Mileage
    etat = Column(SQLEnum(CarStatus), default=CarStatus.AVAILABLE)  # Status
    prix_location = Column(Float, nullable=False)  # Rental price
    image_filename = Column(String, nullable=True)  # Image filename

    # Relationships
    rentals = relationship("Rental", back_populates="car")

    def __repr__(self):
        return f"<Car {self.num_imma} - {self.marque} {self.modele}>"


class Customer(Base):
    """Customer model"""
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    id_loc = Column(String, unique=True, index=True, nullable=False)  # Customer ID
    nom = Column(String, nullable=False)  # Last name
    prenom = Column(String, nullable=False)  # First name
    adresse = Column(String)  # Address

    # Relationships
    rentals = relationship("Rental", back_populates="customer")

    def __repr__(self):
        return f"<Customer {self.id_loc} - {self.prenom} {self.nom}>"


class Rental(Base):
    """Rental model"""
    __tablename__ = "rentals"

    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey("cars.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    date_debut = Column(DateTime, default=datetime.utcnow)  # Start date
    date_fin = Column(DateTime, nullable=True)  # End date (null if not returned)
    date_retour = Column(DateTime, nullable=True)  # Return date

    # Relationships
    car = relationship("Car", back_populates="rentals")
    customer = relationship("Customer", back_populates="rentals")

    def __repr__(self):
        return f"<Rental Car:{self.car_id} - Customer:{self.customer_id}>"
