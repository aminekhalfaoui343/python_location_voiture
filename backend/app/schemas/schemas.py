from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class CarStatusEnum(str, Enum):
    AVAILABLE = "available"
    RENTED = "rented"


# Car Schemas
class CarBase(BaseModel):
    """Base car schema"""
    num_imma: str = Field(..., min_length=1, description="License plate number")
    marque: str = Field(..., min_length=1, description="Car brand")
    modele: str = Field(..., min_length=1, description="Car model")
    kilometrage: int = Field(default=0, ge=0, description="Mileage in km")
    etat: CarStatusEnum = CarStatusEnum.AVAILABLE
    prix_location: float = Field(..., gt=0, description="Rental price per day")
    image_filename: Optional[str] = Field(default=None, description="Car image filename")


class CarCreate(CarBase):
    """Schema for creating a car"""
    pass


class CarUpdate(BaseModel):
    """Schema for updating a car"""
    marque: Optional[str] = None
    modele: Optional[str] = None
    kilometrage: Optional[int] = None
    etat: Optional[CarStatusEnum] = None
    prix_location: Optional[float] = None


class CarResponse(CarBase):
    """Schema for car response"""
    id: int

    class Config:
        from_attributes = True


# Customer Schemas
class CustomerBase(BaseModel):
    """Base customer schema"""
    id_loc: str = Field(..., min_length=1, description="Customer ID")
    nom: str = Field(..., min_length=1, description="Last name")
    prenom: str = Field(..., min_length=1, description="First name")
    adresse: Optional[str] = None


class CustomerCreate(CustomerBase):
    """Schema for creating a customer"""
    pass


class CustomerUpdate(BaseModel):
    """Schema for updating a customer"""
    nom: Optional[str] = None
    prenom: Optional[str] = None
    adresse: Optional[str] = None


class CustomerResponse(CustomerBase):
    """Schema for customer response"""
    id: int

    class Config:
        from_attributes = True


# Rental Schemas
class RentalBase(BaseModel):
    """Base rental schema"""
    car_id: int
    customer_id: int


class RentalCreate(RentalBase):
    """Schema for creating a rental"""
    pass


class RentalReturn(BaseModel):
    """Schema for returning a rental"""
    id: int
    date_retour: Optional[datetime] = None


class RentalResponse(RentalBase):
    """Schema for rental response"""
    id: int
    date_debut: datetime
    date_fin: Optional[datetime] = None
    date_retour: Optional[datetime] = None

    class Config:
        from_attributes = True


class RentalDetail(RentalResponse):
    """Detailed rental response with car and customer info"""
    car: CarResponse
    customer: CustomerResponse


# Statistics Schema
class StatisticsResponse(BaseModel):
    """Schema for statistics response"""
    total_cars: int
    available_cars: int
    rented_cars: int
    average_mileage: float


# Health Check
class HealthResponse(BaseModel):
    """Schema for health check response"""
    status: str
    timestamp: datetime
