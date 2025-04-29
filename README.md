# ColdStore API Documentation

## Project Overview
ColdStore is a Django REST Framework API designed to connect farmers with cold storage owners. It provides secure authentication, geolocation services, and advanced features for managing cold storage facilities.

---

## Key Features
### 1. Multi-Type Authentication System
- **Farmer Registration**: Secure signup with email verification.
- **Storage Owner Portal**: Dashboard for managing cold room operations.
- **Social Authentication**: Google OAuth 2.0 integration with Knox token generation.
- **JWT Refresh Tokens**: Secure token rotation mechanism.

### 2. Advanced Geolocation Services
- Real-time cold room discovery within configurable radii (1-50km).
- Distance-based sorting using PostGIS.
- Capacity filtering (small/medium/large storage).

---

## API Documentation

### Authentication Endpoints
#### 1. User Registration
**Endpoint**: `POST /api/v1/auth/register/`

**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "password2": "SecurePass123!",
  "user_type": "FARMER",
  "phone": "+254712345678",
  "location": {
    "lat": -1.2921,
    "lng": 36.8219
  }
}
```

**Responses**:
- **201 Created**: User successfully registered.
  ```json
  {"user": {...}, "token": "xyz"}
  ```
- **400 Bad Request**: Validation error.
  ```json
  {"email": ["Already exists"]}
  ```

#### 2. Google OAuth Flow
**Endpoint**: `GET /api/v1/auth/google/`

**Flow**:
1. Redirect to Google Auth:
   ```
   https://accounts.google.com/o/oauth2/v2/auth?
     client_id=YOUR_CLIENT_ID
     &redirect_uri=http://localhost:8000/api/v1/auth/google/
     &response_type=code
     &scope=email%20profile
   ```
2. Handle callback with code exchange.
3. Returns Knox token.

**Success Response**:
```json
{
  "user": {
    "id": 1,
    "email": "user@gmail.com",
    "user_type": "FARMER"
  },
  "token": "knox_xyz123"
}
```

---

### Geolocation Endpoints
#### 1. Nearby Cold Rooms
**Endpoint**: `GET /api/v1/coldrooms/nearby/`

**Parameters**:
| Param    | Required | Description                     |
|----------|----------|---------------------------------|
| `lat`    | Yes      | Center latitude                |
| `lng`    | Yes      | Center longitude               |
| `radius` | No       | Search radius in km (default: 10) |
| `capacity` | No     | `small`/`medium`/`large`       |

**Response**:
```json
{
  "results": [
    {
      "id": 1,
      "name": "Nairobi Cold Storage",
      "distance": "2.3 km",
      "capacity": "medium",
      "price_per_kg": 50,
      "rating": 4.5
    }
  ]
}
```

---

## Testing Procedures

### 1. Unit Testing
Run all tests:
```bash
python manage.py test
```

Run specific app tests:
```bash
python manage.py test users.tests.AuthTestCase
```

**Example Test Case**:
```python
class AuthTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_login(self):
        response = self.client.post(
            '/api/v1/auth/login/',
            {'email': 'test@example.com', 'password': 'testpass123'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)
```

### 2. Integration Testing
- Import the ColdStore Postman Collection.
- Set environment variables:
  ```json
  {
    "base_url": "http://localhost:8000",
    "test_email": "testuser@example.com",
    "test_password": "TestPass123!"
  }
  ```

### 3. Google OAuth Testing
**Automated Test Script**:
```python
class GoogleOAuthTest(APITestCase):
    @patch('requests.post')
    def test_google_auth(self, mock_post):
        mock_post.return_value.json.return_value = {
            'access_token': 'mock_token'
        }
        
        response = self.client.get(
            '/api/v1/auth/google/?code=mock_code'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)
```

---

## Deployment Guide

### Production Checklist
- **Security Settings**:
  ```python
  DEBUG = False
  ALLOWED_HOSTS = ['yourdomain.com']
  CSRF_COOKIE_SECURE = True
  SESSION_COOKIE_SECURE = True
  ```

- **Performance Optimization**:
  ```bash
  pip install django-redis hiredis
  ```

- **Monitoring**:
  ```bash
  pip install sentry-sdk
  ```

### Docker Production Setup
**Dockerfile**:
```dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements/prod.txt \
    && apt-get update \
    && apt-get install -y --no-install-recommends gcc python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "coldstore.wsgi:application"]
```

### CI/CD Pipeline
**GitHub Actions Workflow**:
```yaml
name: Django CI

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        ports: ["5432:5432"]
    
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.13'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run tests
        env:
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/postgres
        run: |
          python manage.py test
```

---

## Troubleshooting Guide
| Issue                     | Solution                                      |
|---------------------------|----------------------------------------------|
| OAuth 400 errors          | Verify callback URLs in Google Cloud         |
| PostGIS connection fail   | Check Postgres extensions are enabled        |
| Knox token expiration     | Review REST_KNOX settings                    |

---

## Roadmap
- **v1.1**: SMS Authentication.
- **v1.2**: Cold Room Booking System.
- **v2.0**: Mobile Wallet Integration.

---

## License
This project is licensed under the MIT License.

