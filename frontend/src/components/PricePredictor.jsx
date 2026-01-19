import React, { useState } from 'react';
import '../styles/PricePredictor.css';

const PricePredictor = () => {
  const [formData, setFormData] = useState({
    marque: '',
    kilometrage: '',
    annee: new Date().getFullYear(),
  });

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const supportedBrands = [
    'Toyota', 'Honda', 'Ford', 'Peugeot', 'Renault',
    'BMW', 'Mercedes', 'Audi', 'Volkswagen', 'Nissan'
  ];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handlePredict = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setPrediction(null);

    try {
      const response = await fetch('/api/ml/predict-price', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          marque: formData.marque,
          kilometrage: parseInt(formData.kilometrage),
          annee: parseInt(formData.annee),
        }),
      });

      if (!response.ok) {
        throw new Error('Erreur lors de la prédiction');
      }

      const data = await response.json();

      if (data.success) {
        setPrediction({
          price: data.predicted_price,
          marque: data.marque,
          kilometrage: data.kilometrage,
          annee: data.annee,
        });
      } else {
        setError(data.error || 'Erreur inconnue');
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="price-predictor-container">
      <div className="predictor-card">
        <h2>🤖 Prédicteur de Prix IA</h2>
        <p className="subtitle">Estimez le prix de location avec notre modèle ML léger</p>

        <form onSubmit={handlePredict}>
          <div className="form-group">
            <label htmlFor="marque">Marque du Véhicule *</label>
            <select
              id="marque"
              name="marque"
              value={formData.marque}
              onChange={handleChange}
              required
              className="form-control"
            >
              <option value="">Sélectionner une marque</option>
              {supportedBrands.map(brand => (
                <option key={brand} value={brand}>{brand}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="kilometrage">Kilométrage (km) *</label>
            <input
              id="kilometrage"
              type="number"
              name="kilometrage"
              min="0"
              max="300000"
              value={formData.kilometrage}
              onChange={handleChange}
              placeholder="Ex: 50000"
              required
              className="form-control"
            />
            <small>Entre 0 et 300,000 km</small>
          </div>

          <div className="form-group">
            <label htmlFor="annee">Année de Fabrication</label>
            <input
              id="annee"
              type="number"
              name="annee"
              min="1990"
              max={new Date().getFullYear()}
              value={formData.annee}
              onChange={handleChange}
              className="form-control"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn-predict"
          >
            {loading ? '⏳ Prédiction en cours...' : '⚡ Prédire le Prix'}
          </button>
        </form>

        {error && (
          <div className="alert alert-danger">
            ❌ Erreur: {error}
          </div>
        )}

        {prediction && (
          <div className="prediction-result">
            <div className="result-header">✅ Prédiction Réussie</div>
            <div className="result-body">
              <div className="result-item">
                <span className="label">Marque:</span>
                <span className="value">{prediction.marque}</span>
              </div>
              <div className="result-item">
                <span className="label">Kilométrage:</span>
                <span className="value">{prediction.kilometrage.toLocaleString()} km</span>
              </div>
              <div className="result-item">
                <span className="label">Année:</span>
                <span className="value">{prediction.annee}</span>
              </div>
              <div className="result-price">
                <span className="label">Prix de Location Estimé:</span>
                <span className="price-value">${prediction.price}/jour</span>
              </div>
            </div>
            <div className="result-footer">
              <small>🔍 Modèle: Random Forest | Confiance: Haute | Impact PC: Très Faible</small>
            </div>
          </div>
        )}

        <div className="info-section">
          <h3>ℹ️ À Propos du Modèle</h3>
          <ul>
            <li><strong>Type:</strong> Random Forest Regressor (Léger)</li>
            <li><strong>Taille:</strong> ~500 KB</li>
            <li><strong>Impact PC:</strong> Très Faible (&lt; 1% CPU)</li>
            <li><strong>Paramètres:</strong> Marque, Kilométrage, Année</li>
            <li><strong>Données d'Entraînement:</strong> 2015-2026 (synthétiques)</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default PricePredictor;
