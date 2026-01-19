# Car Rental Management System

A comprehensive full-stack web application for managing car rentals, customers, and vehicles. Built with **FastAPI** (Python backend) and **React + Vite** (modern frontend), featuring **Machine Learning** price prediction and image management capabilities.

## 🎯 Features

### 🚗 Car Management
- ✅ Add, update, and delete cars
- ✅ View car status (available/rented)
- ✅ Track mileage and rental prices
- ✅ Filter cars by availability
- ✅ **Upload and manage car images** (jpg, jpeg, png, gif, webp)
- ✅ Image validation (max 5MB)

### 👤 Customer Management
- ✅ Add, update, and delete customers
- ✅ Search customers by name or ID
- ✅ Display customers sorted alphabetically
- ✅ Manage customer information

### 🔄 Rental Operations
- ✅ Rent cars to customers
- ✅ Return rented cars
- ✅ Enforce business rules (one car per rental, multiple rentals per customer)
- ✅ Track rental history

### 📊 Statistics & Monitoring
- ✅ Dashboard with system overview
- ✅ Total cars, available/rented count
- ✅ Average mileage calculation
- ✅ Health check endpoint

### 🤖 Machine Learning Features
- ✅ **AI-powered rental price prediction**
- ✅ Predict prices based on brand, mileage, and year
- ✅ Random Forest Regressor model
- ✅ Support for 10+ car brands (Toyota, Honda, Ford, Peugeot, Renault, BMW, Mercedes, Audi, Volkswagen, Nissan)
- ✅ Lightweight model (~0.5MB, minimal resource usage)

## 🛠 Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **Pydantic** - Data validation
- **SQLite** - Lightweight database (PostgreSQL-ready)
- **Uvicorn** - ASGI server
- **scikit-learn** - Machine learning library
- **joblib** - Model persistence
- **numpy** - Numerical computing

### Frontend
- **React 18** - UI library
- **Vite** - Build tool
- **Axios** - HTTP client
- **CSS3** - Styling

## 📁 Project Structure

```
car-rental-system/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI app entry point
│   │   ├── database.py             # Database configuration
│   │   ├── routers/
│   │   │   ├── cars.py             # Car endpoints
│   │   │   ├── customers.py        # Customer endpoints
│   │   │   ├── rentals.py          # Rental endpoints
│   │   │   ├── stats.py            # Statistics endpoints
│   │   │   ├── ml.py               # ML prediction endpoints
│   │   │   └── images.py           # Image management endpoints
│   │   ├── schemas/
│   │   │   └── schemas.py          # Pydantic schemas
│   │   ├── models/
│   │   │   └── models.py           # SQLAlchemy models
│   │   └── services/
│   │       ├── car_service.py      # Car business logic
│   │       ├── customer_service.py # Customer business logic
│   │       ├── rental_service.py   # Rental business logic
│   │       └── ml_service.py       # ML prediction logic
│   ├── uploads/
│   │   └── cars/                   # Car images storage
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── main.jsx                # React entry point
│   │   ├── App.jsx                 # Main app component
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx       # Statistics dashboard
│   │   │   ├── CarsPage.jsx        # Car management
│   │   │   ├── CustomersPage.jsx   # Customer management
│   │   │   ├── RentalsPage.jsx     # Rental operations
│   │   │   └── MLPage.jsx          # ML predictions
│   │   ├── components/
│   │   │   ├── Header.jsx
│   │   │   ├── Navigation.jsx
│   │   │   ├── Modal.jsx
│   │   │   ├── ErrorMessage.jsx
│   │   │   ├── SuccessMessage.jsx
│   │   │   └── LoadingSpinner.jsx
│   │   ├── services/
│   │   │   └── api.js              # API client
│   │   └── styles/
│   │       └── global.css
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── Dockerfile
│
├── start-app.bat                   # Windows startup script
├── start-app.sh                    # Linux/Mac startup script
├── docker-compose.yml
├── .gitignore
└── README.md
```

## 🚀 Quick Start

### Option 1: Automated Startup (Recommended)

#### Windows
Simply double-click or run:
```bash
start-app.bat
```

#### Linux/Mac
```bash
chmod +x start-app.sh
./start-app.sh
```

The script will automatically:
- ✅ Check Python and Node.js installation
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Start backend and frontend servers
- ✅ Open the application in your browser

### Option 2: Manual Setup

#### Prerequisites
- Python 3.8+ (Backend)
- Node.js 16+ (Frontend)
- pip and npm

#### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
python -m uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

#### Backend Configuration

**Database Setup:**
- Default: SQLite (`rental_system.db`)
- Optional: PostgreSQL by updating `DATABASE_URL` in `.env`

**Production Mode:**
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**CORS Configuration:**
Update in `app/main.py` for production:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Backend Dependencies:**
- fastapi==0.104.1
- uvicorn==0.24.0
- pydantic==2.5.0
- sqlalchemy==2.0.23
- python-multipart==0.0.6
- python-dateutil==2.8.2
- scikit-learn==1.3.2
- joblib==1.3.2
- numpy==1.24.3

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

#### Frontend Configuration

**Vite Settings:**
- Port: 5173
- Backend Proxy: http://localhost:8000

**API Configuration:**
Update `src/services/api.js` for production:
```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

**Available Scripts:**
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

**Frontend Dependencies:**
- react@^18.2.0
- react-dom@^18.2.0
- react-router-dom@^6.20.0
- axios@^1.6.0

## 📡 API Endpoints

### Cars
- `GET /api/cars` - Get all cars
- `GET /api/cars/{id}` - Get car by ID
- `POST /api/cars` - Create new car
- `PUT /api/cars/{id}` - Update car
- `DELETE /api/cars/{id}` - Delete car
- `GET /api/cars/search/available` - Get available cars
- `GET /api/cars/search/rented` - Get rented cars

### Customers
- `GET /api/customers` - Get all customers (sorted)
- `GET /api/customers/{id}` - Get customer by ID
- `POST /api/customers` - Create new customer
- `PUT /api/customers/{id}` - Update customer
- `DELETE /api/customers/{id}` - Delete customer
- `GET /api/customers/search/by-name?q=query` - Search by name
- `GET /api/customers/search/by-id-loc/{id}` - Search by customer ID

### Rentals
- `GET /api/rentals` - Get all rentals
- `GET /api/rentals/{id}` - Get rental details
- `POST /api/rentals` - Create new rental
- `POST /api/rentals/{id}/return` - Return car
- `DELETE /api/rentals/{id}` - Delete rental
- `GET /api/rentals/search/active` - Get active rentals
- `GET /api/rentals/search/customer/{id}` - Get customer rental history
- `GET /api/rentals/search/car/{id}` - Get car rental history

### Statistics & Health
- `GET /api/statistics` - Get system statistics
- `GET /api/health` - Health check

### Machine Learning
- `POST /api/ml/predict-price` - Predict rental price based on car features
- `GET /api/ml/supported-marques` - Get list of supported car brands
- `GET /api/ml/ml-info` - Get ML model information

### Image Management
- `POST /api/images/cars/{car_id}` - Upload car image (max 5MB)
- `GET /api/images/cars/{car_id}/download` - Download car image
- `DELETE /api/images/cars/{car_id}` - Delete car image

## 🔑 Key Business Rules

1. **Car Rental**: A car can only be rented if its status is "available"
2. **Car Status**: Automatically changes to "rented" when rental is created
3. **Car Return**: Status changes back to "available" when car is returned
4. **Multiple Rentals**: A customer can rent multiple cars simultaneously
5. **Single Renter**: A car can only be rented by one customer at a time
6. **Image Upload**: Only jpg, jpeg, png, gif, webp formats allowed (max 5MB)

## 🛡 Error Handling

The API provides proper HTTP status codes:
- `200 OK` - Success
- `201 Created` - Resource created
- `204 No Content` - Deletion successful
- `400 Bad Request` - Invalid input
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## 🐳 Docker Support

### Using Docker Compose

Run the entire application with one command:
```bash
docker-compose up
```

This will start:
- Backend API at `http://localhost:8000`
- Frontend at `http://localhost:80`

### Backend Dockerfile
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/app ./app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

### Frontend Dockerfile
```dockerfile
FROM node:18-alpine as build
WORKDIR /app
COPY frontend/package*.json .
RUN npm install
COPY frontend .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## 🔄 Data Models

### Car
```python
- id: int (Primary Key)
- num_imma: str (Unique License Plate)
- marque: str (Brand)
- modele: str (Model)
- kilometrage: int (Mileage in km)
- etat: enum (available | rented)
- prix_location: float (Price per day)
- image_filename: str (Image filename, optional)
```

### Customer
```python
- id: int (Primary Key)
- id_loc: str (Unique Customer ID)
- nom: str (Last Name)
- prenom: str (First Name)
- adresse: str (Address, optional)
```

### Rental
```python
- id: int (Primary Key)
- car_id: int (Foreign Key to Car)
- customer_id: int (Foreign Key to Customer)
- date_debut: datetime (Rental start)
- date_fin: datetime (Rental end, optional)
- date_retour: datetime (Return date, optional)
```

## 🤖 Machine Learning Model

### Price Prediction
The system uses a **Random Forest Regressor** to predict optimal rental prices based on:
- **Car Brand** - 10+ supported brands
- **Mileage** - Current vehicle mileage (0-300,000 km)
- **Year** - Vehicle manufacturing year (1990-2026)

### Model Specifications
- **Algorithm**: Random Forest Regressor
- **Estimators**: 50 trees
- **Max Depth**: 10
- **Model Size**: ~0.5 MB
- **Performance Impact**: Minimal (<1% CPU, <50MB RAM)

### Supported Car Brands
Toyota, Honda, Ford, Peugeot, Renault, BMW, Mercedes, Audi, Volkswagen, Nissan

### Example Usage
```bash
curl -X POST "http://localhost:8000/api/ml/predict-price" \
  -H "Content-Type: application/json" \
  -d '{
    "marque": "Toyota",
    "kilometrage": 50000,
    "annee": 2020
  }'
```

## 📝 Environment Variables

Create a `.env` file in the backend directory:

```
DATABASE_URL=sqlite:///./rental_system.db
# For PostgreSQL: postgresql://user:password@localhost/dbname
DEBUG=True
```

## 🧪 Testing

### Backend Testing
```bash
# Test health check
curl http://localhost:8000/api/health

# Get statistics
curl http://localhost:8000/api/statistics

# Test ML prediction
curl -X POST http://localhost:8000/api/ml/predict-price \
  -H "Content-Type: application/json" \
  -d '{"marque": "Toyota", "kilometrage": 50000, "annee": 2020}'
```

### Frontend Testing
Open browser and navigate to `http://localhost:5173`

## 📦 Production Build

### Frontend
```bash
cd frontend
npm run build
# Output in frontend/dist/
```

### Backend
```bash
# Run with production settings
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 🚀 Deployment

### Using Docker Compose
The included `docker-compose.yml` provides:
- Automated container orchestration
- Health checks for both services
- Volume persistence for database
- Network isolation
- Dependency management

Run with: `docker-compose up`

## 📚 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Vite Documentation](https://vitejs.dev/)
- [scikit-learn Documentation](https://scikit-learn.org/)

## 🎓 Academic Use

This project is designed for:
- Academic learning of full-stack development
- DevOps and containerization concepts
- REST API design principles
- Modern frontend architecture
- Database design and ORM usage
- Machine Learning integration in web applications
- Image upload and file management

## 📄 License

This project is provided for educational purposes.

## 👨‍💻 Authors

Created as a comprehensive full-stack application for car rental management with AI-powered features.

---

**Happy coding! 🚀**
"# python_location_voiture" 
