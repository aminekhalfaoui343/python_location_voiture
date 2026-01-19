from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.models import Customer
from app.schemas.schemas import CustomerCreate, CustomerUpdate


class CustomerService:
    """Service layer for customer operations"""

    @staticmethod
    def create_customer(db: Session, customer: CustomerCreate) -> Customer:
        """Create a new customer"""
        db_customer = Customer(**customer.dict())
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        return db_customer

    @staticmethod
    def get_customer(db: Session, customer_id: int) -> Customer:
        """Get customer by ID"""
        return db.query(Customer).filter(Customer.id == customer_id).first()

    @staticmethod
    def get_customer_by_id_loc(db: Session, id_loc: str) -> Customer:
        """Get customer by customer ID"""
        return db.query(Customer).filter(Customer.id_loc == id_loc).first()

    @staticmethod
    def get_customer_by_name(db: Session, nom: str, prenom: str) -> Customer:
        """Get customer by name"""
        return db.query(Customer).filter(
            (Customer.nom == nom) & (Customer.prenom == prenom)
        ).first()

    @staticmethod
    def get_all_customers(db: Session, skip: int = 0, limit: int = 100):
        """Get all customers with pagination, sorted alphabetically"""
        return db.query(Customer).order_by(Customer.nom, Customer.prenom).offset(skip).limit(limit).all()

    @staticmethod
    def get_customers_sorted(db: Session):
        """Get all customers sorted alphabetically by name"""
        return db.query(Customer).order_by(Customer.nom, Customer.prenom).all()

    @staticmethod
    def search_customers(db: Session, query: str):
        """Search customers by name or ID"""
        search_term = f"%{query}%"
        return db.query(Customer).filter(
            (Customer.nom.ilike(search_term)) |
            (Customer.prenom.ilike(search_term)) |
            (Customer.id_loc.ilike(search_term))
        ).all()

    @staticmethod
    def update_customer(db: Session, customer_id: int, customer_update: CustomerUpdate) -> Customer:
        """Update customer details"""
        db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if db_customer:
            update_data = customer_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_customer, field, value)
            db.commit()
            db.refresh(db_customer)
        return db_customer

    @staticmethod
    def delete_customer(db: Session, customer_id: int) -> bool:
        """Delete a customer"""
        db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if db_customer:
            db.delete(db_customer)
            db.commit()
            return True
        return False

    @staticmethod
    def get_total_customers(db: Session) -> int:
        """Count total customers"""
        return db.query(Customer).count()
