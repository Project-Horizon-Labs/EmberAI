# Fire Perimeter Module

This module handles fire perimeter data ingestion and processing for the EmberAI wildfire detection system.

## Files

- **`fire_perimeter_service.py`** - Core service for fetching fire perimeter data from NIFC/WFIGS APIs
- **`api_integration_example.py`** - FastAPI integration example with REST endpoints
- **`fire_demo.py`** - Demonstration script showing service capabilities
- **`__init__.py`** - Package initialization file

## Quick Start

```python
from fire_perimeter import FirePerimeterService, FirePerimeterType

# Initialize service
fire_service = FirePerimeterService()

# Get current fires
current_fires = fire_service.get_fire_perimeters(
    perimeter_type=FirePerimeterType.CURRENT,
    min_acres=100
)

# Get high-priority fires for ember analysis
priority_fires = fire_service.get_high_priority_fires(
    min_acres=1000,
    max_containment=50
)

# Get fires near specific coordinates
nearby_fires = fire_service.get_fires_by_coordinates(
    latitude=34.0522,   # Los Angeles
    longitude=-118.2437,
    radius_miles=100
)
```

## API Endpoints

When using the FastAPI integration, the following endpoints are available:

- `GET /api/fires/current` - Get current active fires
- `GET /api/fires/high-priority` - Get high-priority fires
- `GET /api/fires/nearby` - Get fires near coordinates
- `GET /api/fires/danger-zones` - Get fires with ember risk analysis
- `GET /api/fires/stats` - Get fire statistics
- `GET /health` - Health check endpoint

## Data Sources

- **NIFC/WFIGS APIs** - National Interagency Fire Center
- **Current Perimeters** - Updated every 15-30 minutes
- **Historical Data** - Multi-year fire history
- **No API Key Required** - Uses public endpoints

## Features

- Real-time fire perimeter data
- Geographic filtering (state, bounding box, coordinates)
- Fire size and containment filtering
- Ember risk analysis
- Async support for high-performance applications
- Data persistence and caching
- Comprehensive error handling

## Usage in EmberAI

This module provides the foundation for:
1. **Fire Detection** - Identifying active fires for monitoring
2. **Ember Risk Assessment** - Analyzing fires for spotfire potential
3. **Danger Zone Mapping** - Creating buffer zones around high-risk fires
4. **Drone Coordination** - Providing fire locations for patrol planning
5. **Weather Integration** - Base data for atmospheric modeling

## Running the Demo

```bash
cd backend/fire_perimeter
python fire_demo.py
```

## Starting the API Server

```bash
cd backend/fire_perimeter
python api_integration_example.py
```

The API will be available at `http://localhost:8000` with interactive documentation at `http://localhost:8000/docs`.
