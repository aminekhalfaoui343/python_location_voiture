import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Cars API
export const carsAPI = {
  getAll: (skip = 0, limit = 100) => apiClient.get('/cars', { params: { skip, limit } }),
  getById: (id) => apiClient.get(`/cars/${id}`),
  create: (data) => apiClient.post('/cars', data),
  update: (id, data) => apiClient.put(`/cars/${id}`, data),
  delete: (id) => apiClient.delete(`/cars/${id}`),
  getAvailable: () => apiClient.get('/cars/search/available'),
  getRented: () => apiClient.get('/cars/search/rented'),
};

// Customers API
export const customersAPI = {
  getAll: (skip = 0, limit = 100) => apiClient.get('/customers', { params: { skip, limit } }),
  getById: (id) => apiClient.get(`/customers/${id}`),
  create: (data) => apiClient.post('/customers', data),
  update: (id, data) => apiClient.put(`/customers/${id}`, data),
  delete: (id) => apiClient.delete(`/customers/${id}`),
  searchByName: (query) => apiClient.get('/customers/search/by-name', { params: { q: query } }),
  searchById: (id_loc) => apiClient.get(`/customers/search/by-id-loc/${id_loc}`),
};

// Rentals API
export const rentalsAPI = {
  getAll: (skip = 0, limit = 100) => apiClient.get('/rentals', { params: { skip, limit } }),
  getById: (id) => apiClient.get(`/rentals/${id}`),
  create: (data) => apiClient.post('/rentals', data),
  returnCar: (id, data) => apiClient.post(`/rentals/${id}/return`, data),
  delete: (id) => apiClient.delete(`/rentals/${id}`),
  getActive: () => apiClient.get('/rentals/search/active'),
  getByCustomer: (customerId) => apiClient.get(`/rentals/search/customer/${customerId}`),
  getByCar: (carId) => apiClient.get(`/rentals/search/car/${carId}`),
};

// Statistics API
export const statsAPI = {
  getStatistics: () => apiClient.get('/statistics'),
  healthCheck: () => apiClient.get('/health'),
};

export default apiClient;
