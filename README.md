# Facial Recognition-Based Employee Attendance System

A working prototype for Koffee Lounge Restaurant that uses PostgreSQL, FastAPI, and facial recognition to manage employee attendance.

## Features
- Admin login
- Employee registration with face image upload
- Face recognition-based clock-in and clock-out
- Duplicate attendance prevention
- Attendance report generation
- PostgreSQL database integration
- Simple web dashboard for testing

## Tech Stack
- Backend: Python + FastAPI
- Frontend: HTML + JavaScript
- Database: PostgreSQL
- Face recognition: OpenCV + face_recognition
- Authentication: JWT

## Project Structure
- `backend/app` – API and database logic
- `frontend/static` – dashboard UI
- `db/schema.sql` – database schema
- `docker-compose.yml` – PostgreSQL container setup

## Setup Instructions

### 1. Create virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Start PostgreSQL
```bash
docker compose up -d
```

### 4. Configure environment
Create a `.env` file using `.env.example`:
```bash
cp .env.example .env
```

### 5. Create database tables
```bash
python -c "from backend.app.database import Base, engine; from backend.app import models; Base.metadata.create_all(bind=engine)"
```

### 6. Start the API
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 7. Access the app
Open:
```text
http://localhost:8000/
```

## Default admin login
- Username: `admin`
- Password: `admin123`

## Notes
This prototype is intended for testing and academic demonstration. It uses a local PostgreSQL instance and a simple camera-driven recognition workflow for attendance marking.
