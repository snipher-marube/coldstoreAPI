# ColdStore API - Documentation

## Project Overview
ColdStore is a Django REST Framework API designed to connect farmers with cold storage owners. It provides the following features:

- **User Authentication**: Supports Farmers and Cold Room Owners.
- **Geolocation Services**: Enables discovery of nearby cold rooms.
- **Secure API Endpoints**: Implements Knox token-based authentication.
- **Social Authentication**: Optional Google OAuth integration.

---

## Features

### 1. Authentication System
- **User Types**:
  - Farmers (`FARMER`)
  - Cold Room Owners (`COLD_ROOM_OWNER`)
- **Authentication Methods**:
  - Email/password registration
  - Knox token-based authentication
  - Google OAuth (optional)

### 2. Geolocation Services
- Discover cold rooms within a 10km radius.
- Powered by PostgreSQL + PostGIS for spatial queries.
- Google Maps API integration.

### 3. API Endpoints
| Endpoint                  | Method | Description                  |
|---------------------------|--------|------------------------------|
| `/api/v1/auth/register/`  | POST   | User registration            |
| `/api/v1/auth/login/`     | POST   | User login                   |
| `/api/v1/auth/logout/`    | POST   | Token invalidation           |
| `/api/v1/coldrooms/nearby/` | GET   | Find nearby cold rooms       |

---

## Technical Stack

### Backend
- **Language**: Python 3.13
- **Framework**: Django 5.1
- **Libraries**:
  - Django REST Framework
  - Django REST Knox (Token Authentication)
  - PostgreSQL with PostGIS (Geospatial Queries)
  - Redis (Caching)

### Frontend (Optional)
- React/Next.js
- Flutter (Mobile App)

---

## Installation Guide

### Prerequisites
- Python 3.13+
- PostgreSQL 15+
- Redis (for caching)

### Setup Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/coldstore-api.git
   cd coldstore-api
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv .env
   source .env/bin/activate  # Linux/Mac
   .env\Scripts\activate    # Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**
   ```bash
   sudo -u postgres psql
   CREATE DATABASE coldstore;
   CREATE USER coldstore_user WITH PASSWORD 'yourpassword';
   GRANT ALL PRIVILEGES ON DATABASE coldstore TO coldstore_user;
   ```

5. **Environment Variables**
   Create a `.env` file with the following content:
   ```ini
   SECRET_KEY=your-secret-key
   DB_NAME=coldstore
   DB_USER=coldstore_user
   DB_PASSWORD=yourpassword
   DB_HOST=localhost
   DB_PORT=5432
   GOOGLE_OAUTH_CLIENT_ID=your-client-id
   ```

6. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

7. **Start Development Server**
   ```bash
   python manage.py runserver
   ```

---

## API Documentation
Explore API endpoints with Swagger UI:
http://localhost:8000/api/v1/docs/

---

## Testing
Run tests with:
```bash
python manage.py test
```

---

## Deployment

### Production Setup

1. **Gunicorn (WSGI Server)**
   ```bash
   pip install gunicorn
   gunicorn coldstore.wsgi:application --bind 0.0.0.0:8000
   ```

2. **Nginx Configuration**
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
       }
       
       location /static/ {
           alias /path/to/your/staticfiles/;
       }
   }
   ```

3. **Docker Setup (Optional)**
   ```dockerfile
   FROM python:3.13
   WORKDIR /app
   COPY . .
   RUN pip install -r requirements.txt
   CMD ["gunicorn", "coldstore.wsgi:application", "--bind", "0.0.0.0:8000"]
   ```

---

## Project Structure
```plaintext
coldstore/
├── coldstore/          # Project config
├── users/              # Auth app
│   ├── models.py       # Custom User model
│   ├── serializers.py  # Auth serializers
│   └── views.py        # Auth views
├── locations/          # Geolocation app
│   ├── models.py       # ColdRoom model
│   └── views.py        # Location views
├── requirements/       # Dependency files
└── manage.py           # Django CLI
```

---

## Contributing
1. Fork the repository.
2. Create your feature branch:
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Open a Pull Request.

---

## License
MIT License - See LICENSE for details.

---

## Support
For issues or questions, please open an issue.

---

Happy Coding! 🎉

