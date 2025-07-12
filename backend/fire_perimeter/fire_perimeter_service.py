"""
Fire Perimeter Service for EmberAI
Handles ingestion of fire perimeter data from NIFC/WFIGS APIs
"""

import requests
import json
import logging
from typing import Dict, List, Optional, Union
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import asyncio
import aiohttp
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FirePerimeterType(Enum):
    """Types of fire perimeter data available"""
    CURRENT = "current"
    YEAR_TO_DATE = "ytd"
    CERTIFIED = "certified"
    HISTORICAL = "historical"


@dataclass
class FirePerimeter:
    """Data class for fire perimeter information"""
    incident_id: str
    incident_name: str
    geometry: Dict
    acres: float
    containment_percent: int
    discovery_date: datetime
    state: str
    county: str
    fire_cause: str
    fire_behavior: str
    poi_latitude: float
    poi_longitude: float
    suppression_method: str
    initial_response_acres: float
    total_personnel: int
    structures_threatened: int
    structures_destroyed: int
    fire_management_complexity: str
    estimated_cost: float
    fire_origin: str
    weather_concerns: str
    fuel_model: str
    fire_danger_rating: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "incident_id": self.incident_id,
            "incident_name": self.incident_name,
            "geometry": self.geometry,
            "acres": self.acres,
            "containment_percent": self.containment_percent,
            "discovery_date": self.discovery_date.isoformat() if self.discovery_date else None,
            "state": self.state,
            "county": self.county,
            "fire_cause": self.fire_cause,
            "fire_behavior": self.fire_behavior,
            "poi_latitude": self.poi_latitude,
            "poi_longitude": self.poi_longitude,
            "suppression_method": self.suppression_method,
            "initial_response_acres": self.initial_response_acres,
            "total_personnel": self.total_personnel,
            "structures_threatened": self.structures_threatened,
            "structures_destroyed": self.structures_destroyed,
            "fire_management_complexity": self.fire_management_complexity,
            "estimated_cost": self.estimated_cost,
            "fire_origin": self.fire_origin,
            "weather_concerns": self.weather_concerns,
            "fuel_model": self.fuel_model,
            "fire_danger_rating": self.fire_danger_rating
        }


class FirePerimeterService:
    """Service for fetching fire perimeter data from NIFC/WFIGS APIs"""
    
    def __init__(self):
        self.base_url = "https://services3.arcgis.com/T4QMspbfLg3qTGWY/ArcGIS/rest/services"
        self.endpoints = {
            FirePerimeterType.CURRENT: f"{self.base_url}/WFIGS_Interagency_Perimeters_Current/FeatureServer/0/query",
            FirePerimeterType.YEAR_TO_DATE: f"{self.base_url}/WFIGS_Interagency_Perimeters_YearToDate/FeatureServer/0/query",
            FirePerimeterType.CERTIFIED: f"{self.base_url}/WFIGS_Interagency_Perimeters_Certified/FeatureServer/0/query",
            FirePerimeterType.HISTORICAL: f"{self.base_url}/InterAgencyFirePerimeterHistory_All_Years_View/FeatureServer/0/query"
        }
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'EmberAI-FirePerimeter-Service/1.0'
        })
    
    def get_fire_perimeters(self, 
                          perimeter_type: FirePerimeterType = FirePerimeterType.CURRENT,
                          bbox: Optional[str] = None,
                          state_code: Optional[str] = None,
                          min_acres: Optional[int] = None,
                          max_age_days: Optional[int] = None) -> Dict:
        """
        Get fire perimeters with various filtering options
        
        Args:
            perimeter_type: Type of perimeter data to fetch
            bbox: Bounding box filter "xmin,ymin,xmax,ymax" (WGS84)
            state_code: Two-letter state code (e.g., 'CA', 'CO')
            min_acres: Minimum fire size in acres
            max_age_days: Maximum age of fires in days
        
        Returns:
            GeoJSON FeatureCollection of fire perimeters
        """
        try:
            endpoint = self.endpoints[perimeter_type]
            params = self._build_query_params(bbox, state_code, min_acres, max_age_days)
            
            logger.info(f"Fetching {perimeter_type.value} fire perimeters")
            response = self.session.get(endpoint, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Retrieved {len(data.get('features', []))} fire perimeters")
            
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching fire perimeters: {str(e)}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON response: {str(e)}")
            raise
    
    def get_fires_by_coordinates(self, 
                               latitude: float, 
                               longitude: float, 
                               radius_miles: float = 50,
                               perimeter_type: FirePerimeterType = FirePerimeterType.CURRENT) -> Dict:
        """
        Get fires within a specified radius of coordinates
        
        Args:
            latitude: Latitude in decimal degrees
            longitude: Longitude in decimal degrees
            radius_miles: Search radius in miles
            perimeter_type: Type of perimeter data to fetch
        
        Returns:
            GeoJSON FeatureCollection of nearby fire perimeters
        """
        # Convert miles to degrees (approximate)
        degree_radius = radius_miles / 69.0  # 1 degree ≈ 69 miles
        
        bbox = f"{longitude - degree_radius},{latitude - degree_radius},{longitude + degree_radius},{latitude + degree_radius}"
        
        return self.get_fire_perimeters(perimeter_type, bbox=bbox)
    
    def get_high_priority_fires(self, 
                              min_acres: int = 1000,
                              max_containment: int = 50,
                              structures_threatened: int = 1) -> Dict:
        """
        Get high-priority fires for ember spotfire analysis
        
        Args:
            min_acres: Minimum fire size in acres
            max_containment: Maximum containment percentage
            structures_threatened: Minimum structures threatened
        
        Returns:
            GeoJSON FeatureCollection of high-priority fires
        """
        try:
            endpoint = self.endpoints[FirePerimeterType.CURRENT]
            
            # Build complex where clause for high-priority fires
            where_conditions = [
                f"DailyAcres >= {min_acres}",
                f"PercentContained <= {max_containment}",
                f"StructuresThreated >= {structures_threatened}"
            ]
            
            params = {
                'where': ' AND '.join(where_conditions),
                'outFields': '*',
                'f': 'geojson',
                'orderByFields': 'DailyAcres DESC'
            }
            
            logger.info("Fetching high-priority fires for ember analysis")
            response = self.session.get(endpoint, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Retrieved {len(data.get('features', []))} high-priority fires")
            
            return data
            
        except Exception as e:
            logger.error(f"Error fetching high-priority fires: {str(e)}")
            raise
    
    def get_fire_growth_analysis(self, days_back: int = 7) -> Dict:
        """
        Analyze fire growth over the past specified days
        
        Args:
            days_back: Number of days to look back for growth analysis
        
        Returns:
            Analysis of fire growth patterns
        """
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            # Get current fires
            current_fires = self.get_fire_perimeters(FirePerimeterType.CURRENT)
            
            # Get historical data for comparison
            historical_fires = self.get_fire_perimeters(FirePerimeterType.YEAR_TO_DATE)
            
            # Analyze growth patterns
            growth_analysis = self._analyze_fire_growth(current_fires, historical_fires, start_date)
            
            return growth_analysis
            
        except Exception as e:
            logger.error(f"Error analyzing fire growth: {str(e)}")
            raise
    
    def parse_fire_features(self, geojson_data: Dict) -> List[FirePerimeter]:
        """
        Parse GeoJSON features into FirePerimeter objects
        
        Args:
            geojson_data: GeoJSON FeatureCollection from API
        
        Returns:
            List of FirePerimeter objects
        """
        fire_perimeters = []
        
        for feature in geojson_data.get('features', []):
            properties = feature.get('properties', {})
            geometry = feature.get('geometry', {})
            
            try:
                fire_perimeter = FirePerimeter(
                    incident_id=properties.get('IRWINID', ''),
                    incident_name=properties.get('IncidentName', ''),
                    geometry=geometry,
                    acres=float(properties.get('DailyAcres', 0)),
                    containment_percent=int(properties.get('PercentContained', 0)),
                    discovery_date=self._parse_date(properties.get('FireDiscoveryDateTime')),
                    state=properties.get('POOState', ''),
                    county=properties.get('POOCounty', ''),
                    fire_cause=properties.get('FireCause', ''),
                    fire_behavior=properties.get('FireBehaviorGeneral', ''),
                    poi_latitude=float(properties.get('InitialLatitude', 0)),
                    poi_longitude=float(properties.get('InitialLongitude', 0)),
                    suppression_method=properties.get('SuppressionMethod', ''),
                    initial_response_acres=float(properties.get('InitialResponseAcres', 0)),
                    total_personnel=int(properties.get('TotalPersonnel', 0)),
                    structures_threatened=int(properties.get('StructuresThreated', 0)),
                    structures_destroyed=int(properties.get('StructuresDestroyed', 0)),
                    fire_management_complexity=properties.get('FireMgmtComplexity', ''),
                    estimated_cost=float(properties.get('EstimatedCostToDate', 0)),
                    fire_origin=properties.get('FireOrigin', ''),
                    weather_concerns=properties.get('WeatherConcerns', ''),
                    fuel_model=properties.get('FuelModel', ''),
                    fire_danger_rating=properties.get('FireDangerRating', '')
                )
                
                fire_perimeters.append(fire_perimeter)
                
            except (ValueError, TypeError) as e:
                logger.warning(f"Error parsing fire feature: {str(e)}")
                continue
        
        return fire_perimeters
    
    def save_fire_data(self, fire_perimeters: List[FirePerimeter], filename: str = None) -> Path:
        """
        Save fire perimeter data to JSON file
        
        Args:
            fire_perimeters: List of FirePerimeter objects
            filename: Optional filename, auto-generated if not provided
        
        Returns:
            Path to saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"fire_perimeters_{timestamp}.json"
        
        filepath = Path(__file__).parent / "data" / filename
        filepath.parent.mkdir(exist_ok=True)
        
        data = {
            "timestamp": datetime.now().isoformat(),
            "count": len(fire_perimeters),
            "fires": [fire.to_dict() for fire in fire_perimeters]
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Saved {len(fire_perimeters)} fire perimeters to {filepath}")
        return filepath
    
    def _build_query_params(self, 
                          bbox: Optional[str] = None,
                          state_code: Optional[str] = None,
                          min_acres: Optional[int] = None,
                          max_age_days: Optional[int] = None) -> Dict:
        """Build query parameters for API request"""
        params = {
            'where': '1=1',
            'outFields': '*',
            'f': 'geojson'
        }
        
        where_conditions = []
        
        if state_code:
            where_conditions.append(f"POOState='{state_code.upper()}'")
        
        if min_acres:
            where_conditions.append(f"DailyAcres >= {min_acres}")
        
        if max_age_days:
            cutoff_date = datetime.now() - timedelta(days=max_age_days)
            date_str = cutoff_date.strftime("%Y-%m-%d")
            where_conditions.append(f"FireDiscoveryDateTime >= '{date_str}'")
        
        if where_conditions:
            params['where'] = ' AND '.join(where_conditions)
        
        if bbox:
            params['geometry'] = bbox
            params['geometryType'] = 'esriGeometryEnvelope'
            params['spatialRel'] = 'esriSpatialRelIntersects'
        
        return params
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse date string from API response"""
        if not date_str:
            return None
        
        try:
            # Handle various date formats from the API
            if date_str.isdigit():
                # Unix timestamp in milliseconds
                return datetime.fromtimestamp(int(date_str) / 1000)
            else:
                # ISO format
                return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except (ValueError, TypeError):
            logger.warning(f"Could not parse date: {date_str}")
            return None
    
    def _analyze_fire_growth(self, current_fires: Dict, historical_fires: Dict, start_date: datetime) -> Dict:
        """Analyze fire growth patterns"""
        # This is a placeholder for more sophisticated growth analysis
        # In a real implementation, you would compare fire sizes over time
        
        current_count = len(current_fires.get('features', []))
        historical_count = len(historical_fires.get('features', []))
        
        return {
            "analysis_date": datetime.now().isoformat(),
            "current_active_fires": current_count,
            "total_ytd_fires": historical_count,
            "growth_rate": "Analysis placeholder - implement detailed growth tracking",
            "high_growth_fires": [],
            "ember_risk_fires": []
        }


class AsyncFirePerimeterService:
    """Async version of FirePerimeterService for concurrent requests"""
    
    def __init__(self):
        self.base_url = "https://services3.arcgis.com/T4QMspbfLg3qTGWY/ArcGIS/rest/services"
        self.endpoints = {
            FirePerimeterType.CURRENT: f"{self.base_url}/WFIGS_Interagency_Perimeters_Current/FeatureServer/0/query",
            FirePerimeterType.YEAR_TO_DATE: f"{self.base_url}/WFIGS_Interagency_Perimeters_YearToDate/FeatureServer/0/query",
            FirePerimeterType.CERTIFIED: f"{self.base_url}/WFIGS_Interagency_Perimeters_Certified/FeatureServer/0/query"
        }
    
    async def get_fire_perimeters_async(self, 
                                      perimeter_type: FirePerimeterType = FirePerimeterType.CURRENT,
                                      **kwargs) -> Dict:
        """Async version of get_fire_perimeters"""
        
        async with aiohttp.ClientSession() as session:
            endpoint = self.endpoints[perimeter_type]
            params = self._build_query_params(**kwargs)
            
            async with session.get(endpoint, params=params) as response:
                response.raise_for_status()
                data = await response.json()
                
                logger.info(f"Retrieved {len(data.get('features', []))} fire perimeters (async)")
                return data
    
    async def get_multiple_fire_types_async(self, 
                                          perimeter_types: List[FirePerimeterType],
                                          **kwargs) -> Dict[FirePerimeterType, Dict]:
        """Fetch multiple fire perimeter types concurrently"""
        
        tasks = []
        for perimeter_type in perimeter_types:
            task = self.get_fire_perimeters_async(perimeter_type, **kwargs)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        
        return dict(zip(perimeter_types, results))
    
    def _build_query_params(self, **kwargs) -> Dict:
        """Build query parameters (same as sync version)"""
        params = {
            'where': '1=1',
            'outFields': '*',
            'f': 'geojson'
        }
        
        # Add filtering logic similar to sync version
        # ... (implementation details)
        
        return params


# Example usage and testing
if __name__ == "__main__":
    # Initialize the service
    fire_service = FirePerimeterService()
    
    # Example 1: Get current fires in California
    print("Fetching current fires in California...")
    ca_fires = fire_service.get_fire_perimeters(
        perimeter_type=FirePerimeterType.CURRENT,
        state_code="CA",
        min_acres=100
    )
    print(f"Found {len(ca_fires.get('features', []))} fires in California")
    
    # Example 2: Get high-priority fires
    print("\nFetching high-priority fires...")
    priority_fires = fire_service.get_high_priority_fires(min_acres=1000)
    print(f"Found {len(priority_fires.get('features', []))} high-priority fires")
    
    # Example 3: Get fires near a specific location (e.g., Los Angeles)
    print("\nFetching fires near Los Angeles...")
    la_fires = fire_service.get_fires_by_coordinates(
        latitude=34.0522,
        longitude=-118.2437,
        radius_miles=100
    )
    print(f"Found {len(la_fires.get('features', []))} fires near Los Angeles")
    
    # Example 4: Parse and save fire data
    if ca_fires.get('features'):
        fire_objects = fire_service.parse_fire_features(ca_fires)
        saved_path = fire_service.save_fire_data(fire_objects)
        print(f"Saved fire data to {saved_path}")
