from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional
import logging
from datetime import datetime
from fire_perimeter import FirePerimeterService, FirePerimeterType

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="EmberAI Wildfire Detection API", version="1.0.0")

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize fire perimeter service
fire_service = FirePerimeterService()

@app.get("/")
def read_root():
    return {"message": "EmberAI Wildfire Detection API running!", "version": "1.0.0"}

# LIVE FIRE DATA ROUTES
@app.get("/api/fires/live/current")
async def get_live_current_fires(
    state: Optional[str] = Query(None, description="Two-letter state code (e.g., 'CA', 'TX')"),
    min_acres: Optional[int] = Query(None, description="Minimum fire size in acres"),
    max_age_days: Optional[int] = Query(None, description="Maximum fire age in days"),
    bbox: Optional[str] = Query(None, description="Bounding box 'xmin,ymin,xmax,ymax'")
):
    """Get live/current active fires with optional filtering"""
    try:
        fires = fire_service.get_fire_perimeters(
            perimeter_type=FirePerimeterType.CURRENT,
            state_code=state,
            min_acres=min_acres,
            max_age_days=max_age_days,
            bbox=bbox
        )
        
        return JSONResponse(content=fires)
        
    except Exception as e:
        logger.error(f"Error fetching live current fires: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/fires/live/high-priority")
async def get_live_high_priority_fires(
    min_acres: int = Query(1000, description="Minimum fire size in acres"),
    max_containment: int = Query(50, description="Maximum containment percentage"),
    structures_threatened: int = Query(1, description="Minimum structures threatened")
):
    """Get live high-priority fires for ember spotfire analysis"""
    try:
        fires = fire_service.get_high_priority_fires(
            min_acres=min_acres,
            max_containment=max_containment,
            structures_threatened=structures_threatened
        )
        
        return JSONResponse(content=fires)
        
    except Exception as e:
        logger.error(f"Error fetching live high-priority fires: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/fires/live/nearby")
async def get_live_nearby_fires(
    latitude: float = Query(..., description="Latitude in decimal degrees"),
    longitude: float = Query(..., description="Longitude in decimal degrees"),
    radius_miles: float = Query(50, description="Search radius in miles")
):
    """Get live fires within a specified radius of coordinates"""
    try:
        fires = fire_service.get_fires_by_coordinates(
            latitude=latitude,
            longitude=longitude,
            radius_miles=radius_miles
        )
        
        return JSONResponse(content=fires)
        
    except Exception as e:
        logger.error(f"Error fetching live nearby fires: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/fires/live/stats")
async def get_live_fire_statistics():
    """Get summary statistics for live fire activity"""
    try:
        # Get current fires
        current_fires = fire_service.get_fire_perimeters(FirePerimeterType.CURRENT)
        
        # Calculate statistics
        features = current_fires.get('features', [])
        
        if not features:
            return JSONResponse(content={
                "total_fires": 0,
                "total_acres": 0,
                "avg_acres_per_fire": 0,
                "states_affected": 0,
                "largest_fire": None,
                "timestamp": datetime.now().isoformat()
            })
        
        total_acres = sum(feature.get('properties', {}).get('DailyAcres', 0) for feature in features)
        states = set(feature.get('properties', {}).get('POOState', '') for feature in features)
        
        # Find largest fire
        largest_fire = max(features, key=lambda x: x.get('properties', {}).get('DailyAcres', 0))
        largest_fire_info = {
            "name": largest_fire.get('properties', {}).get('IncidentName', 'Unknown'),
            "acres": largest_fire.get('properties', {}).get('DailyAcres', 0),
            "state": largest_fire.get('properties', {}).get('POOState', 'Unknown'),
            "containment": largest_fire.get('properties', {}).get('PercentContained', 0)
        }
        
        stats = {
            "total_fires": len(features),
            "total_acres": total_acres,
            "avg_acres_per_fire": total_acres / len(features) if features else 0,
            "states_affected": len(states),
            "largest_fire": largest_fire_info,
            "timestamp": datetime.now().isoformat()
        }
        
        return JSONResponse(content=stats)
        
    except Exception as e:
        logger.error(f"Error calculating live fire statistics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# HISTORICAL FIRE DATA ROUTES
@app.get("/api/fires/historical/perimeters")
async def get_historical_fire_perimeters(
    state: Optional[str] = Query(None, description="Two-letter state code"),
    min_acres: Optional[int] = Query(1000, description="Minimum fire size in acres"),
    bbox: Optional[str] = Query(None, description="Bounding box 'xmin,ymin,xmax,ymax'")
):
    """Get historical fire perimeter data"""
    try:
        fires = fire_service.get_fire_perimeters(
            perimeter_type=FirePerimeterType.HISTORICAL,
            state_code=state,
            min_acres=min_acres,
            bbox=bbox
        )
        
        return JSONResponse(content=fires)
        
    except Exception as e:
        logger.error(f"Error fetching historical fires: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/fires/historical/year-to-date")
async def get_year_to_date_fires(
    state: Optional[str] = Query(None, description="Two-letter state code"),
    min_acres: Optional[int] = Query(500, description="Minimum fire size in acres"),
    bbox: Optional[str] = Query(None, description="Bounding box 'xmin,ymin,xmax,ymax'")
):
    """Get year-to-date fire data"""
    try:
        fires = fire_service.get_fire_perimeters(
            perimeter_type=FirePerimeterType.YEAR_TO_DATE,
            state_code=state,
            min_acres=min_acres,
            bbox=bbox
        )
        
        return JSONResponse(content=fires)
        
    except Exception as e:
        logger.error(f"Error fetching year-to-date fires: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/fires/historical/certified")
async def get_certified_fire_perimeters(
    state: Optional[str] = Query(None, description="Two-letter state code"),
    min_acres: Optional[int] = Query(1000, description="Minimum fire size in acres"),
    bbox: Optional[str] = Query(None, description="Bounding box 'xmin,ymin,xmax,ymax'")
):
    """Get certified fire perimeter data"""
    try:
        fires = fire_service.get_fire_perimeters(
            perimeter_type=FirePerimeterType.CERTIFIED,
            state_code=state,
            min_acres=min_acres,
            bbox=bbox
        )
        
        return JSONResponse(content=fires)
        
    except Exception as e:
        logger.error(f"Error fetching certified fires: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# EMBER ANALYSIS ROUTES
@app.get("/api/ember/danger-zones")
async def get_ember_danger_zones(
    state: Optional[str] = Query(None, description="Two-letter state code"),
    min_acres: int = Query(500, description="Minimum fire size for danger zone analysis"),
    wind_speed_threshold: float = Query(15.0, description="Wind speed threshold (mph) for ember transport")
):
    """Get fires that pose ember spotfire danger"""
    try:
        # Get fires that are large enough and not fully contained
        fires = fire_service.get_high_priority_fires(
            min_acres=min_acres,
            max_containment=80,  # Less than 80% contained
            structures_threatened=0  # Any structures
        )
        
        # Enhanced ember risk analysis
        if fires and fires.get('features'):
            for feature in fires['features']:
                properties = feature.get('properties', {})
                
                # Add ember risk assessment
                acres = properties.get('DailyAcres', 0)
                containment = properties.get('PercentContained', 0)
                
                # Risk scoring algorithm
                risk_score = 0
                if acres > 5000:
                    risk_score += 3
                elif acres > 1000:
                    risk_score += 2
                else:
                    risk_score += 1
                
                if containment < 25:
                    risk_score += 2
                elif containment < 50:
                    risk_score += 1
                
                properties['ember_risk_score'] = risk_score
                properties['ember_risk_level'] = 'HIGH' if risk_score >= 4 else 'MEDIUM' if risk_score >= 2 else 'LOW'
                properties['danger_zone_radius_miles'] = min(risk_score * 2, 10)  # Max 10 miles
                properties['analysis_timestamp'] = datetime.now().isoformat()
        
        return JSONResponse(content=fires)
        
    except Exception as e:
        logger.error(f"Error generating ember danger zones: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# HEALTH CHECK
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test API connectivity
        test_fires = fire_service.get_fire_perimeters(FirePerimeterType.CURRENT)
        
        return JSONResponse(content={
            "status": "healthy",
            "api_connectivity": "ok",
            "fire_service": "operational",
            "timestamp": datetime.now().isoformat(),
            "active_fires_count": len(test_fires.get('features', []))
        })
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e),
                "api_connectivity": "failed",
                "timestamp": datetime.now().isoformat()
            }
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
