# ColdStore API - Documentation

## Project Overview
ColdStore is a Django REST Framework API designed to connect farmers with cold storage owners. It provides the following key features:

- **User Authentication**: Supports Farmers and Cold Room Owners.
- **Geolocation Services**: Enables discovery of nearby cold rooms.
- **Secure API Endpoints**: Implements Knox token-based authentication.
- **Social Authentication**: Google OAuth integration for seamless login.

---

## Features

### 1. Authentication System
- **User Types**:
  - Farmers (`FARMER`)
  - Cold Room Owners (`COLD_ROOM_OWNER`)
- **Authentication Methods**:
  - Email/password registration
  - Knox token-based authentication
  - Google OAuth integration

### 2. Geolocation Services
- Discover cold rooms within a 10km radius.
- Powered by PostgreSQL + PostGIS for spatial queries.

---

## API Documentation

### Authentication Endpoints

#### 1. User Registration
**Endpoint**: `POST /api/v1/auth/register/`  
**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "password2": "securepassword123",
  "user_type": "FARMER" | "COLD_ROOM_OWNER"
}
```