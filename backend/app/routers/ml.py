from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ml_service import predict_rental_price, MARQUES

router = APIRouter(prefix="/api/ml", tags=["ML Predictions"])


class PricePredictor(BaseModel):
    """Modèle pour la prédiction de prix"""
    marque: str
    kilometrage: int
    annee: int = 2023


class PredictionResponse(BaseModel):
    """Réponse de prédiction"""
    success: bool
    predicted_price: float = None
    marque: str = None
    kilometrage: int = None
    annee: int = None
    confidence: str = None
    error: str = None


@router.post("/predict-price", response_model=PredictionResponse)
async def predict_price(data: PricePredictor):
    """
    Prédit le prix de location d'une voiture basé sur ses caractéristiques
    
    - **marque**: Marque du véhicule (ex: Toyota, Honda, Ford, etc.)
    - **kilometrage**: Kilométrage actuel (0-300000)
    - **annee**: Année de fabrication (optionnel, défaut: 2023)
    
    Marques supportées: Toyota, Honda, Ford, Peugeot, Renault, BMW, Mercedes, Audi, Volkswagen, Nissan
    """
    
    # Validation
    if not data.marque or not data.marque.strip():
        raise HTTPException(status_code=400, detail="La marque est requise")
    
    if data.kilometrage < 0 or data.kilometrage > 300000:
        raise HTTPException(status_code=400, detail="Kilométrage doit être entre 0 et 300000")
    
    if data.annee < 1990 or data.annee > 2026:
        raise HTTPException(status_code=400, detail="Année doit être entre 1990 et 2026")

    result = predict_rental_price(
        marque=data.marque,
        kilometrage=data.kilometrage,
        annee=data.annee
    )

    return result


@router.get("/supported-marques")
async def get_supported_marques():
    """Retourne la liste des marques supportées par le modèle ML"""
    return {
        "supported_marques": MARQUES,
        "count": len(MARQUES)
    }


@router.get("/ml-info")
async def get_ml_info():
    """Informations sur le modèle ML"""
    return {
        "model_type": "Random Forest Regressor",
        "features": ["Marque du véhicule", "Kilométrage", "Âge du véhicule"],
        "n_estimators": 50,
        "max_depth": 10,
        "size_mb": "~0.5",
        "impact_pc": "Très faible (< 1% CPU, < 50MB RAM)",
        "supported_marques": MARQUES
    }
