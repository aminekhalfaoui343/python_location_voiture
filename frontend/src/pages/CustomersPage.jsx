import React, { useState, useEffect } from 'react';
import { customersAPI } from '../services/api';
import Modal from '../components/Modal';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import SuccessMessage from '../components/SuccessMessage';

function CustomersPage() {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [editingCustomer, setEditingCustomer] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [formData, setFormData] = useState({
    id_loc: '',
    nom: '',
    prenom: '',
    adresse: '',
  });

  useEffect(() => {
    fetchCustomers();
  }, []);

  const fetchCustomers = async () => {
    try {
      setLoading(true);
      const response = await customersAPI.getAll();
      setCustomers(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load customers: ' + (err.response?.data?.detail || err.message));
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      fetchCustomers();
      return;
    }
    try {
      const response = await customersAPI.searchByName(searchQuery);
      setCustomers(response.data);
    } catch (err) {
      setError('Customer not found');
    }
  };

  const handleOpenModal = (customer = null) => {
    if (customer) {
      setEditingCustomer(customer);
      setFormData(customer);
    } else {
      setEditingCustomer(null);
      setFormData({
        id_loc: '',
        nom: '',
        prenom: '',
        adresse: '',
      });
    }
    setModalOpen(true);
  };

  const handleCloseModal = () => {
    setModalOpen(false);
    setEditingCustomer(null);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async () => {
    if (!formData.id_loc || !formData.nom || !formData.prenom) {
      setError('Please fill in all required fields');
      return;
    }

    try {
      if (editingCustomer) {
        await customersAPI.update(editingCustomer.id, formData);
        setSuccess('Customer updated successfully!');
      } else {
        await customersAPI.create(formData);
        setSuccess('Customer added successfully!');
      }
      handleCloseModal();
      fetchCustomers();
    } catch (err) {
      setError('Failed to save customer: ' + (err.response?.data?.detail || err.message));
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this customer?')) {
      try {
        await customersAPI.delete(id);
        setSuccess('Customer deleted successfully!');
        fetchCustomers();
      } catch (err) {
        setError('Failed to delete customer: ' + (err.response?.data?.detail || err.message));
      }
    }
  };

  if (loading && customers.length === 0) return <LoadingSpinner />;

  return (
    <div className="page">
      <h2>Customers Management</h2>
      {error && <ErrorMessage message={error} onClose={() => setError(null)} />}
      {success && <SuccessMessage message={success} onClose={() => setSuccess(null)} />}

      <div className="controls-section">
        <button className="btn btn-success" onClick={() => handleOpenModal()}>
          ➕ Add New Customer
        </button>
        
        <div className="search-box">
          <input
            type="text"
            placeholder="Search customer by name or ID..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
          />
          <button className="btn btn-primary" onClick={handleSearch}>Search</button>
          <button className="btn btn-secondary" onClick={() => { setSearchQuery(''); fetchCustomers(); }}>Clear</button>
        </div>
      </div>

      <div className="table-responsive">
        <table className="data-table">
          <thead>
            <tr>
              <th>Customer ID</th>
              <th>First Name</th>
              <th>Last Name</th>
              <th>Address</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {customers.map(customer => (
              <tr key={customer.id}>
                <td><strong>{customer.id_loc}</strong></td>
                <td>{customer.prenom}</td>
                <td>{customer.nom}</td>
                <td>{customer.adresse || 'N/A'}</td>
                <td>
                  <button className="btn btn-sm btn-primary" onClick={() => handleOpenModal(customer)}>
                    Edit
                  </button>
                  <button className="btn btn-sm btn-danger" onClick={() => handleDelete(customer.id)}>
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <Modal
        isOpen={modalOpen}
        title={editingCustomer ? 'Edit Customer' : 'Add New Customer'}
        onClose={handleCloseModal}
        onSubmit={handleSubmit}
      >
        <form>
          <div className="form-group">
            <label>Customer ID *</label>
            <input
              type="text"
              name="id_loc"
              value={formData.id_loc}
              onChange={handleInputChange}
              placeholder="e.g., C001"
              disabled={editingCustomer !== null}
            />
          </div>
          <div className="form-group">
            <label>First Name *</label>
            <input
              type="text"
              name="prenom"
              value={formData.prenom}
              onChange={handleInputChange}
              placeholder="John"
            />
          </div>
          <div className="form-group">
            <label>Last Name *</label>
            <input
              type="text"
              name="nom"
              value={formData.nom}
              onChange={handleInputChange}
              placeholder="Doe"
            />
          </div>
          <div className="form-group">
            <label>Address</label>
            <input
              type="text"
              name="adresse"
              value={formData.adresse}
              onChange={handleInputChange}
              placeholder="123 Main St"
            />
          </div>
        </form>
      </Modal>
    </div>
  );
}

export default CustomersPage;
