import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import os
import logging

logger = logging.getLogger(__name__)

# Chemin du modèle
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../../models/price_model.pkl")
ENCODER_PATH = os.path.join(os.path.dirname(__file__), "../../models/encoder.pkl")

# Marques communes
MARQUES = ["Toyota", "Honda", "Ford", "Peugeot", "Renault", "BMW", "Mercedes", "Audi", "Volkswagen", "Nissan"]


def train_model():
    """Entraîne le modèle ML avec des données synthétiques"""
    try:
        # Créer les dossiers s'ils n'existent pas
        models_dir = os.path.dirname(MODEL_PATH)
        os.makedirs(models_dir, exist_ok=True)

        # Données synthétiques d'entraînement
        X_train = []
        y_train = []

        # Générer des données synthétiques
        for marque_idx, marque in enumerate(MARQUES):
            for km in range(10000, 200000, 20000):
                for annee in range(2015, 2024):
                    # Features: [marque_encoded, kilométrage, année]
                    age_voiture = 2026 - annee
                    prix_base = 50
                    
                    # Logique de prix
                    prix = prix_base - (km * 0.01) - (age_voiture * 2) + (marque_idx * 3)
                    prix = max(prix, 20)  # Prix minimum
                    
                    X_train.append([marque_idx, km, age_voiture])
                    y_train.append(prix)

        X_train = np.array(X_train)
        y_train = np.array(y_train)

        # Entraîner le modèle
        model = RandomForestRegressor(
            n_estimators=50,  # Léger
            max_depth=10,
            random_state=42,
            n_jobs=1
        )
        model.fit(X_train, y_train)

        # Sauvegarder le modèle
        joblib.dump(model, MODEL_PATH)
        logger.info(f"Modèle entraîné et sauvegardé à {MODEL_PATH}")

        return model

    except Exception as e:
        logger.error(f"Erreur lors de l'entraînement du modèle: {e}")
        return None


def load_model():
    """Charge le modèle ML"""
    try:
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
            return model
        else:
            logger.info("Modèle non trouvé, entraînement d'un nouveau modèle...")
            return train_model()
    except Exception as e:
        logger.error(f"Erreur lors du chargement du modèle: {e}")
        return None


def encode_marque(marque: str) -> int:
    """Encode la marque en nombre"""
    try:
        return MARQUES.index(marque.capitalize())
    except ValueError:
        return 0  # Valeur par défaut


def predict_rental_price(marque: str, kilometrage: int, annee: int = 2023) -> dict:
    """
    Prédit le prix de location d'une voiture
    
    Args:
        marque: Marque du véhicule
        kilometrage: Kilométrage du véhicule
        annee: Année de fabrication
    
    Returns:
        dict avec la prédiction de prix
    """
    try:
        model = load_model()
        
        if model is None:
            return {
                "success": False,
                "error": "Modèle ML non disponible",
                "predicted_price": None
            }

        # Préparer les features
        marque_encoded = encode_marque(marque)
        age_voiture = 2026 - annee
        
        # Vérifier les limites
        kilometrage = max(0, min(kilometrage, 300000))
        age_voiture = max(0, min(age_voiture, 50))

        features = np.array([[marque_encoded, kilometrage, age_voiture]])

        # Prédiction
        predicted_price = float(model.predict(features)[0])
        predicted_price = max(20.0, predicted_price)  # Prix minimum

        return {
            "success": True,
            "predicted_price": round(predicted_price, 2),
            "marque": marque,
            "kilometrage": kilometrage,
            "annee": annee,
            "confidence": "Modèle léger (Random Forest)"
        }

    except Exception as e:
        logger.error(f"Erreur lors de la prédiction: {e}")
        return {
            "success": False,
            "error": str(e),
            "predicted_price": None
        }


# Charger le modèle au démarrage
_model = load_model()
