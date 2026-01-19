from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
import shutil
from datetime import datetime
import uuid

from app.database import get_db
from app.models.models import Car

router = APIRouter(prefix="/api/images", tags=["images"])

# Create uploads directory
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '../../uploads/cars')
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Allowed extensions
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}


def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@router.post("/cars/{car_id}")
async def upload_car_image(
    car_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload image for a car"""
    
    # Check if car exists
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename")
    
    if not allowed_file(file.filename):
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Limit file size (5MB)
    contents = await file.read()
    if len(contents) > 5 * 1024 * 1024:  # 5MB
        raise HTTPException(status_code=400, detail="File too large (max 5MB)")
    
    try:
        # Create unique filename
        file_ext = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"car_{car_id}_{uuid.uuid4().hex}.{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        # Save file
        with open(file_path, 'wb') as f:
            f.write(contents)
        
        # Delete old image if exists
        if car.image_filename:
            old_path = os.path.join(UPLOAD_DIR, car.image_filename)
            if os.path.exists(old_path):
                os.remove(old_path)
        
        # Update car
        car.image_filename = unique_filename
        db.commit()
        
        return {
            "status": "success",
            "message": "Image uploaded successfully",
            "filename": unique_filename,
            "url": f"/api/images/cars/{car_id}/download"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("/cars/{car_id}/download")
async def download_car_image(car_id: int, db: Session = Depends(get_db)):
    """Download car image"""
    
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car or not car.image_filename:
        raise HTTPException(status_code=404, detail="Image not found")
    
    file_path = os.path.join(UPLOAD_DIR, car.image_filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image file not found")
    
    return FileResponse(file_path, media_type='image/*')


@router.delete("/cars/{car_id}")
async def delete_car_image(car_id: int, db: Session = Depends(get_db)):
    """Delete car image"""
    
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    
    if not car.image_filename:
        raise HTTPException(status_code=404, detail="No image to delete")
    
    try:
        file_path = os.path.join(UPLOAD_DIR, car.image_filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        car.image_filename = None
        db.commit()
        
        return {
            "status": "success",
            "message": "Image deleted successfully"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")
