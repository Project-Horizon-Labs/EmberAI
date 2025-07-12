"""
FastAPI integration example for Fire Perimeter Service
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Optional, List
import logging
from datetime import datetime
from .fire_perimeter_service import FirePerimeterService, FirePerimeterType, AsyncFirePerimeterService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="EmberAI Fire Perimeter API", version="1.0.0")

# Initialize services
fire_service = FirePerimeterService()
async_fire_service = AsyncFirePerimeterService()


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "EmberAI Fire Perimeter API", "version": "1.0.0"}


@app.get("/api/fires/current")
async def get_current_fires(
    state: Optional[str] = Query(None, description="Two-letter state code (e.g., 'CA', 'TX')"),
    min_acres: Optional[int] = Query(None, description="Minimum fire size in acres"),
    max_age_days: Optional[int] = Query(None, description="Maximum fire age in days"),
    bbox: Optional[str] = Query(None, description="Bounding box 'xmin,ymin,xmax,ymax'")
):
    """Get current active fires with optional filtering"""
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
        logger.error(f"Error fetching current fires: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/fires/high-priority")
async def get_high_priority_fires(
    min_acres: int = Query(1000, description="Minimum fire size in acres"),
    max_containment: int = Query(50, description="Maximum containment percentage"),
    structures_threatened: int = Query(1, description="Minimum structures threatened")
):
    """Get high-priority fires for ember spotfire analysis"""
    try:
        fires = fire_service.get_high_priority_fires(
            min_acres=min_acres,
            max_containment=max_containment,
            structures_threatened=structures_threatened
        )
        
        return JSONResponse(content=fires)
        
    except Exception as e:
        logger.error(f"Error fetching high-priority fires: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/fires/nearby")
async def get_nearby_fires(
    latitude: float = Query(..., description="Latitude in decimal degrees"),
    longitude: float = Query(..., description="Longitude in decimal degrees"),
    radius_miles: float = Query(50, description="Search radius in miles")
):
    """Get fires within a specified radius of coordinates"""
    try:
        fires = fire_service.get_fires_by_coordinates(
            latitude=latitude,
            longitude=longitude,
            radius_miles=radius_miles
        )
        
        return JSONResponse(content=fires)
        
    except Exception as e:
        logger.error(f"Error fetching nearby fires: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/fires/danger-zones")
async def get_danger_zones(
    state: Optional[str] = Query(None, description="Two-letter state code"),
    min_acres: int = Query(500, description="Minimum fire size for danger zone analysis"),
    wind_speed_threshold: float = Query(15.0, description="Wind speed threshold (mph) for ember transport")
):
    """
    Get fires that pose ember spotfire danger
    This is a simplified version - in production, you'd integrate with weather data
    """
    try:
        # Get fires that are large enough and not fully contained
        fires = fire_service.get_high_priority_fires(
            min_acres=min_acres,
            max_containment=80,  # Less than 80% contained
            structures_threatened=0  # Any structures
        )
        
        # In a real implementation, you would:
        # 1. Get weather data for each fire location
        # 2. Calculate ember transport potential based on wind speed/direction
        # 3. Generate danger zone polygons around fires
        # 4. Return enhanced GeoJSON with danger zones
        
        # For now, just return the fires with additional metadata
        if fires and fires.get('features'):
            for feature in fires['features']:
                properties = feature.get('properties', {})
                
                # Add ember risk assessment (simplified)
                acres = properties.get('DailyAcres', 0)
                containment = properties.get('PercentContained', 0)
                
                # Simple risk scoring
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
        
        return JSONResponse(content=fires)
        
    except Exception as e:
        logger.error(f"Error generating danger zones: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/fires/growth-analysis")
async def get_fire_growth_analysis(
    days_back: int = Query(7, description="Number of days to analyze for growth patterns")
):
    """Analyze fire growth patterns over the specified period"""
    try:
        analysis = fire_service.get_fire_growth_analysis(days_back=days_back)
        
        return JSONResponse(content=analysis)
        
    except Exception as e:
        logger.error(f"Error analyzing fire growth: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/fires/historical")
async def get_historical_fires(
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


@app.get("/api/fires/stats")
async def get_fire_statistics():
    """Get summary statistics for current fire activity"""
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
                "largest_fire": None
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
            "largest_fire": largest_fire_info
        }
        
        return JSONResponse(content=stats)
        
    except Exception as e:
        logger.error(f"Error calculating fire statistics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test API connectivity
        test_fires = fire_service.get_fire_perimeters(FirePerimeterType.CURRENT)
        
        return JSONResponse(content={
            "status": "healthy",
            "api_connectivity": "ok",
            "timestamp": fire_service._parse_date(str(int(datetime.now().timestamp() * 1000))).isoformat() if fire_service._parse_date else "unknown"
        })
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e),
                "api_connectivity": "failed"
            }
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
