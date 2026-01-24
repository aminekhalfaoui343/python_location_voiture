from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import CustomerCreate, CustomerResponse, CustomerUpdate
from app.services.customer_service import CustomerService

router = APIRouter(prefix="/api/customers", tags=["customers"])


@router.post("/", response_model=CustomerResponse, status_code=201)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    """Create a new customer"""
    # Check if customer with same ID already exists
    existing_customer = CustomerService.get_customer_by_id_loc(db, customer.id_loc)
    if existing_customer:
        raise HTTPException(status_code=400, detail="Customer with this ID already exists")

    return CustomerService.create_customer(db, customer)


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    """Get customer by ID"""
    customer = CustomerService.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.get("/", response_model=list[CustomerResponse])
def get_all_customers(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    """Get all customers sorted alphabetically"""
    return CustomerService.get_all_customers(db, skip, limit)


@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: int, customer: CustomerUpdate, db: Session = Depends(get_db)):
    """Update customer details"""
    db_customer = CustomerService.get_customer(db, customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return CustomerService.update_customer(db, customer_id, customer)


@router.delete("/{customer_id}", status_code=204)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    """Delete a customer"""
    success = CustomerService.delete_customer(db, customer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Customer not found")
    return None


@router.get("/search/by-id-loc/{id_loc}", response_model=CustomerResponse)
def get_customer_by_id_loc(id_loc: str, db: Session = Depends(get_db)):
    """Search customer by ID"""
    customer = CustomerService.get_customer_by_id_loc(db, id_loc)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.get("/search/by-name", response_model=list[CustomerResponse])
def search_customers(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    """Search customers by name or ID"""
    customers = CustomerService.search_customers(db, q)
    if not customers:
        raise HTTPException(status_code=404, detail="No customers found")
    return customers
