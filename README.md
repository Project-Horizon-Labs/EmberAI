# Wildfire Ember Spotfire Detection and Response

## Overview
This project aims to help firefighters stop wildfire spread from ember-derived spotfires. It combines geospatial modeling, weather/environmental data, and autonomous drones with thermal cameras to detect and tag spot fires.

### Key Components
- **Backend (Python/FastAPI):**
  - Ingests fire perimeter, weather, and environmental data
  - Generates a 'danger zone' map at risk for ember spotfires
  - Handles drone patrol logic, detection, and signaling
- **Frontend (React):**
  - Visualizes the danger zone and drone positions
  - Receives and displays alerts for detected spotfires
  - Provides controls for simulation/demo

### Getting Started
- `backend/`: Python FastAPI server
- `frontend/`: React app

#### Prerequisites
- Python 3.9+
- Node.js 16+

#### Setup
1. Install backend dependencies:
   ```sh
   cd backend
   pip install -r requirements.txt
   ```
2. Install frontend dependencies:
   ```sh
   cd frontend
   npm install
   ```
3. Run backend:
   ```sh
   uvicorn main:app --reload
   ```
4. Run frontend:
   ```sh
   npm start
   ```

---

This is a starter scaffold. Each module will be developed step by step!
