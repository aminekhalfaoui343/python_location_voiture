import React, { useState, useEffect } from 'react';
import { rentalsAPI, carsAPI, customersAPI } from '../services/api';
import Modal from '../components/Modal';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import SuccessMessage from '../components/SuccessMessage';

function RentalsPage() {
  const [rentals, setRentals] = useState([]);
  const [cars, setCars] = useState([]);
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('all');
  const [formData, setFormData] = useState({
    car_id: '',
    customer_id: '',
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [rentalsRes, carsRes, customersRes] = await Promise.all([
        rentalsAPI.getAll(),
        carsAPI.getAll(),
        customersAPI.getAll(),
      ]);
      setRentals(rentalsRes.data);
      setCars(carsRes.data);
      setCustomers(customersRes.data);
      setError(null);
    } catch (err) {
      setError('Failed to load data: ' + (err.response?.data?.detail || err.message));
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleOpenModal = () => {
    setFormData({ car_id: '', customer_id: '' });
    setModalOpen(true);
  };

  const handleCloseModal = () => {
    setModalOpen(false);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: parseInt(value) || ''
    }));
  };

  const handleSubmit = async () => {
    if (!formData.car_id || !formData.customer_id) {
      setError('Please select both a car and a customer');
      return;
    }

    try {
      await rentalsAPI.create(formData);
      setSuccess('Car rented successfully!');
      handleCloseModal();
      fetchData();
    } catch (err) {
      setError('Failed to create rental: ' + (err.response?.data?.detail || err.message));
    }
  };

  const handleReturnCar = async (rentalId) => {
    if (window.confirm('Are you sure you want to return this car?')) {
      try {
        await rentalsAPI.returnCar(rentalId, {});
        setSuccess('Car returned successfully!');
        fetchData();
      } catch (err) {
        setError('Failed to return car: ' + (err.response?.data?.detail || err.message));
      }
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this rental record?')) {
      try {
        await rentalsAPI.delete(id);
        setSuccess('Rental deleted successfully!');
        fetchData();
      } catch (err) {
        setError('Failed to delete rental: ' + (err.response?.data?.detail || err.message));
      }
    }
  };

  const getRentalDisplay = (rental) => {
    const car = cars.find(c => c.id === rental.car_id);
    const customer = customers.find(c => c.id === rental.customer_id);
    return { car, customer };
  };

  const filteredRentals = activeTab === 'active' ? rentals.filter(r => !r.date_retour) : rentals;

  if (loading && rentals.length === 0) return <LoadingSpinner />;

  return (
    <div className="page">
      <h2>Rentals Management</h2>
      {error && <ErrorMessage message={error} onClose={() => setError(null)} />}
      {success && <SuccessMessage message={success} onClose={() => setSuccess(null)} />}

      <button className="btn btn-success" onClick={handleOpenModal}>
        🔄 Create New Rental
      </button>

      <div className="tabs">
        <button 
          className={`tab ${activeTab === 'all' ? 'active' : ''}`}
          onClick={() => setActiveTab('all')}
        >
          All Rentals
        </button>
        <button 
          className={`tab ${activeTab === 'active' ? 'active' : ''}`}
          onClick={() => setActiveTab('active')}
        >
          Active Rentals
        </button>
      </div>

      <div className="table-responsive">
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Car</th>
              <th>Customer</th>
              <th>Start Date</th>
              <th>Return Date</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredRentals.map(rental => {
              const { car, customer } = getRentalDisplay(rental);
              return (
                <tr key={rental.id}>
                  <td>#{rental.id}</td>
                  <td>{car ? `${car.marque} ${car.modele}` : 'N/A'}</td>
                  <td>{customer ? `${customer.prenom} ${customer.nom}` : 'N/A'}</td>
                  <td>{new Date(rental.date_debut).toLocaleDateString()}</td>
                  <td>{rental.date_retour ? new Date(rental.date_retour).toLocaleDateString() : '—'}</td>
                  <td>
                    <span className={`badge ${rental.date_retour ? 'badge-success' : 'badge-warning'}`}>
                      {rental.date_retour ? '✓ Returned' : '⏳ Active'}
                    </span>
                  </td>
                  <td>
                    {!rental.date_retour && (
                      <button className="btn btn-sm btn-success" onClick={() => handleReturnCar(rental.id)}>
                        Return
                      </button>
                    )}
                    <button className="btn btn-sm btn-danger" onClick={() => handleDelete(rental.id)}>
                      Delete
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <Modal
        isOpen={modalOpen}
        title="Create New Rental"
        onClose={handleCloseModal}
        onSubmit={handleSubmit}
      >
        <form>
          <div className="form-group">
            <label>Car *</label>
            <select name="car_id" value={formData.car_id} onChange={handleInputChange}>
              <option value="">Select a car...</option>
              {cars.filter(c => c.etat === 'available').map(car => (
                <option key={car.id} value={car.id}>
                  {car.marque} {car.modele} ({car.num_imma})
                </option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label>Customer *</label>
            <select name="customer_id" value={formData.customer_id} onChange={handleInputChange}>
              <option value="">Select a customer...</option>
              {customers.map(customer => (
                <option key={customer.id} value={customer.id}>
                  {customer.prenom} {customer.nom} ({customer.id_loc})
                </option>
              ))}
            </select>
          </div>
        </form>
      </Modal>
    </div>
  );
}

export default RentalsPage;
