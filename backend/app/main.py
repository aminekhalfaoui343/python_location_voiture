from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.database import init_db
from app.routers import cars, customers, rentals, stats, ml, images

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Car Rental Management System API",
    description="A comprehensive API for managing car rentals, customers, and vehicles",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# CORS Middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(cars.router)
app.include_router(customers.router)
app.include_router(rentals.router)
app.include_router(stats.router)
app.include_router(ml.router)
app.include_router(images.router)

# Root endpoint
@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "Car Rental Management System API",
        "version": "1.0.0",
        "docs": "/api/docs",
        "health": "/api/health"
    }

# Health check endpoint
@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Application is running"
    }

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    """Initialize database on startup"""
    init_db()
    logger.info("Database initialized")

@app.on_event("shutdown")
def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Application shutting down")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
