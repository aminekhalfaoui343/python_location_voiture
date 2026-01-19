import React, { useState, useEffect } from 'react';
import { carsAPI } from '../services/api';
import Modal from '../components/Modal';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import SuccessMessage from '../components/SuccessMessage';
import '../styles/CarsPage.css';

function CarsPage() {
  const [cars, setCars] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [imageModalOpen, setImageModalOpen] = useState(false);
  const [editingCar, setEditingCar] = useState(null);
  const [selectedCarForImage, setSelectedCarForImage] = useState(null);
  const [imageFile, setImageFile] = useState(null);
  const [uploadingImage, setUploadingImage] = useState(false);
  const [formData, setFormData] = useState({
    num_imma: '',
    marque: '',
    modele: '',
    kilometrage: 0,
    prix_location: 0,
  });

  useEffect(() => {
    fetchCars();
  }, []);

  const fetchCars = async () => {
    try {
      setLoading(true);
      const response = await carsAPI.getAll();
      setCars(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load cars: ' + (err.response?.data?.detail || err.message));
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleOpenModal = (car = null) => {
    if (car) {
      setEditingCar(car);
      setFormData(car);
    } else {
      setEditingCar(null);
      setFormData({
        num_imma: '',
        marque: '',
        modele: '',
        kilometrage: 0,
        prix_location: 0,
      });
    }
    setModalOpen(true);
  };

  const handleCloseModal = () => {
    setModalOpen(false);
    setEditingCar(null);
  };

  const handleOpenImageModal = (car) => {
    setSelectedCarForImage(car);
    setImageFile(null);
    setImageModalOpen(true);
  };

  const handleCloseImageModal = () => {
    setImageModalOpen(false);
    setSelectedCarForImage(null);
    setImageFile(null);
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.size > 5 * 1024 * 1024) {
        setError('Image must be less than 5MB');
        return;
      }
      setImageFile(file);
    }
  };

  const handleUploadImage = async () => {
    if (!imageFile || !selectedCarForImage) {
      setError('Please select an image');
      return;
    }

    try {
      setUploadingImage(true);
      const formDataImg = new FormData();
      formDataImg.append('file', imageFile);

      const response = await fetch(`/api/images/cars/${selectedCarForImage.id}`, {
        method: 'POST',
        body: formDataImg,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Upload failed');
      }

      setSuccess('Image uploaded successfully!');
      fetchCars();
      handleCloseImageModal();
    } catch (err) {
      setError('Upload failed: ' + err.message);
    } finally {
      setUploadingImage(false);
    }
  };

  const handleDeleteImage = async (carId) => {
    if (!window.confirm('Delete this image?')) return;

    try {
      const response = await fetch(`/api/images/cars/${carId}`, {
        method: 'DELETE',
      });

      if (!response.ok) throw new Error('Delete failed');

      setSuccess('Image deleted successfully!');
      fetchCars();
    } catch (err) {
      setError('Failed to delete image: ' + err.message);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'kilometrage' || name === 'prix_location' ? parseFloat(value) || 0 : value
    }));
  };

  const handleSubmit = async () => {
    if (!formData.num_imma || !formData.marque || !formData.modele) {
      setError('Please fill in all required fields');
      return;
    }

    try {
      if (editingCar) {
        await carsAPI.update(editingCar.id, formData);
        setSuccess('Car updated successfully!');
      } else {
        await carsAPI.create(formData);
        setSuccess('Car added successfully!');
      }
      handleCloseModal();
      fetchCars();
    } catch (err) {
      setError('Failed to save car: ' + (err.response?.data?.detail || err.message));
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this car?')) {
      try {
        await carsAPI.delete(id);
        setSuccess('Car deleted successfully!');
        fetchCars();
      } catch (err) {
        setError('Failed to delete car: ' + (err.response?.data?.detail || err.message));
      }
    }
  };

  if (loading && cars.length === 0) return <LoadingSpinner />;

  return (
    <div className="cars-page">
      <div className="page-header">
        <h2>🚗 Cars Management</h2>
        <button className="btn btn-primary" onClick={() => handleOpenModal()}>
          + Add New Car
        </button>
      </div>

      {error && <ErrorMessage message={error} onClose={() => setError(null)} />}
      {success && <SuccessMessage message={success} onClose={() => setSuccess(null)} />}

      <div className="cars-grid">
        {cars.map(car => (
          <div key={car.id} className="car-card">
            <div className="car-image-container">
              {car.image_filename ? (
                <>
                  <img
                    src={`/api/images/cars/${car.id}/download`}
                    alt={`${car.marque} ${car.modele}`}
                    className="car-image"
                  />
                  <button
                    className="btn-delete-image"
                    onClick={() => handleDeleteImage(car.id)}
                    title="Delete image"
                  >
                    ✕
                  </button>
                </>
              ) : (
                <div className="car-image-placeholder">
                  <span>📷 No Image</span>
                </div>
              )}
              <button
                className="btn-upload-image"
                onClick={() => handleOpenImageModal(car)}
              >
                📸 Upload
              </button>
            </div>

            <div className="car-details">
              <h3>{car.marque} {car.modele}</h3>
              <p className="license-plate"><strong>{car.num_imma}</strong></p>
              <p><strong>Mileage:</strong> {car.kilometrage.toLocaleString()} km</p>
              <p><strong>Price:</strong> ${car.prix_location.toFixed(2)}/day</p>
              <span className={`badge ${car.etat === 'available' ? 'badge-success' : 'badge-danger'}`}>
                {car.etat === 'available' ? '✓ Available' : '✗ Rented'}
              </span>
            </div>

            <div className="car-actions">
              <button
                className="btn btn-sm btn-primary"
                onClick={() => handleOpenModal(car)}
              >
                ✎ Edit
              </button>
              <button
                className="btn btn-sm btn-danger"
                onClick={() => handleDelete(car.id)}
              >
                🗑 Delete
              </button>
            </div>
          </div>
        ))}
      </div>

      {cars.length === 0 && !loading && (
        <div className="empty-state">
          <p>No cars found. Create your first car!</p>
        </div>
      )}

      {/* Edit Modal */}
      <Modal isOpen={modalOpen} onClose={handleCloseModal} title={editingCar ? 'Edit Car' : 'Add New Car'}>
        <form>
          <div className="form-group">
            <label>License Plate *</label>
            <input
              type="text"
              name="num_imma"
              value={formData.num_imma}
              onChange={handleInputChange}
              placeholder="e.g., AB-123-CD"
              disabled={editingCar !== null}
            />
          </div>
          <div className="form-group">
            <label>Brand *</label>
            <input
              type="text"
              name="marque"
              value={formData.marque}
              onChange={handleInputChange}
              placeholder="e.g., Toyota"
            />
          </div>
          <div className="form-group">
            <label>Model *</label>
            <input
              type="text"
              name="modele"
              value={formData.modele}
              onChange={handleInputChange}
              placeholder="e.g., Corolla"
            />
          </div>
          <div className="form-group">
            <label>Mileage (km)</label>
            <input
              type="number"
              name="kilometrage"
              value={formData.kilometrage}
              onChange={handleInputChange}
              min="0"
            />
          </div>
          <div className="form-group">
            <label>Price per Day ($) *</label>
            <input
              type="number"
              name="prix_location"
              value={formData.prix_location}
              onChange={handleInputChange}
              min="0"
              step="0.01"
            />
          </div>
          <button type="button" className="btn btn-primary" onClick={handleSubmit}>
            Save
          </button>
        </form>
      </Modal>

      {/* Image Upload Modal */}
      <Modal isOpen={imageModalOpen} onClose={handleCloseImageModal} title="Upload Car Image">
        {selectedCarForImage && (
          <div className="image-upload-form">
            <p>Upload image for: <strong>{selectedCarForImage.marque} {selectedCarForImage.modele}</strong></p>
            <input
              type="file"
              accept="image/*"
              onChange={handleImageChange}
              disabled={uploadingImage}
            />
            <small>Max: 5MB. Formats: JPG, PNG, GIF, WebP</small>
            <button
              type="button"
              className="btn btn-primary"
              onClick={handleUploadImage}
              disabled={!imageFile || uploadingImage}
            >
              {uploadingImage ? 'Uploading...' : 'Upload'}
            </button>
          </div>
        )}
      </Modal>
    </div>
  );
}

export default CarsPage;
