"""
Demo script showing historical and live fire perimeter data capabilities
"""

import json
import sys
import os
from datetime import datetime, timedelta

# Add the parent directory to the path so we can import fire_perimeter
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fire_perimeter import FirePerimeterService, FirePerimeterType


def demo_historical_and_live_data():
    """Demonstrate both historical and live fire data capabilities"""
    
    print("🔥 EmberAI Fire Perimeter Data Demo - Historical & Live")
    print("=" * 60)
    
    # Initialize the service
    fire_service = FirePerimeterService()
    
    # 1. Get LIVE/CURRENT fire data
    print("\n1. 📡 LIVE FIRE DATA (Current Active Fires)")
    print("-" * 40)
    try:
        live_fires = fire_service.get_fire_perimeters(
            perimeter_type=FirePerimeterType.CURRENT,
            min_acres=100  # Only fires > 100 acres
        )
        
        live_count = len(live_fires.get('features', []))
        print(f"   ✅ Found {live_count} active fires > 100 acres")
        
        if live_count > 0:
            # Show data format
            sample_fire = live_fires['features'][0]
            print(f"   📄 Data Format: GeoJSON")
            print(f"   🗂️  Sample Fire Properties:")
            
            props = sample_fire.get('properties', {})
            print(f"      • Name: {props.get('IncidentName', 'Unknown')}")
            print(f"      • State: {props.get('POOState', 'Unknown')}")
            print(f"      • Size: {props.get('DailyAcres', 0):,} acres")
            print(f"      • Containment: {props.get('PercentContained', 0)}%")
            print(f"      • Discovery Date: {props.get('FireDiscoveryDateTime', 'Unknown')}")
            
            # Show geometry type
            geometry = sample_fire.get('geometry', {})
            print(f"      • Geometry Type: {geometry.get('type', 'Unknown')}")
            print(f"      • Has Coordinates: {'Yes' if geometry.get('coordinates') else 'No'}")
        
    except Exception as e:
        print(f"   ❌ Error fetching live data: {str(e)}")
    
    # 2. Get HISTORICAL fire data
    print("\n2. 📚 HISTORICAL FIRE DATA (Multi-year Archive)")
    print("-" * 40)
    try:
        historical_fires = fire_service.get_fire_perimeters(
            perimeter_type=FirePerimeterType.HISTORICAL,
            state_code="CA",  # California only for demo
            min_acres=5000    # Large fires only
        )
        
        historical_count = len(historical_fires.get('features', []))
        print(f"   ✅ Found {historical_count} historical fires > 5,000 acres in CA")
        
        if historical_count > 0:
            # Analyze historical data
            fires_by_year = {}
            total_acres = 0
            
            for feature in historical_fires['features']:
                props = feature.get('properties', {})
                
                # Extract year from fire discovery date
                discovery_date = props.get('FireDiscoveryDateTime', '')
                if discovery_date:
                    try:
                        year = discovery_date[:4]  # First 4 characters should be year
                        if year.isdigit():
                            if year not in fires_by_year:
                                fires_by_year[year] = 0
                            fires_by_year[year] += 1
                    except:
                        pass
                
                # Sum total acres
                acres = props.get('DailyAcres', 0) or props.get('GISAcres', 0)
                if acres:
                    total_acres += acres
            
            print(f"   🔥 Total Historical Acres: {total_acres:,} acres")
            print(f"   📅 Years with Data: {len(fires_by_year)} years")
            
            # Show top years
            if fires_by_year:
                sorted_years = sorted(fires_by_year.items(), key=lambda x: x[1], reverse=True)
                print(f"   📊 Top Fire Years:")
                for year, count in sorted_years[:5]:
                    print(f"      • {year}: {count} large fires")
        
    except Exception as e:
        print(f"   ❌ Error fetching historical data: {str(e)}")
    
    # 3. Get YEAR-TO-DATE fire data
    print("\n3. 📅 YEAR-TO-DATE DATA (2025 Fires)")
    print("-" * 40)
    try:
        ytd_fires = fire_service.get_fire_perimeters(
            perimeter_type=FirePerimeterType.YEAR_TO_DATE,
            min_acres=500
        )
        
        ytd_count = len(ytd_fires.get('features', []))
        ytd_acres = sum(f.get('properties', {}).get('DailyAcres', 0) 
                       for f in ytd_fires.get('features', []))
        
        print(f"   ✅ Found {ytd_count} fires > 500 acres in 2025")
        print(f"   🔥 Total YTD Acres: {ytd_acres:,} acres")
        
    except Exception as e:
        print(f"   ❌ Error fetching YTD data: {str(e)}")
    
    # 4. Demonstrate JSON export capabilities
    print("\n4. 💾 JSON EXPORT CAPABILITIES")
    print("-" * 40)
    try:
        # Get a small sample of current fires
        sample_fires = fire_service.get_fire_perimeters(
            perimeter_type=FirePerimeterType.CURRENT,
            min_acres=1000
        )
        
        # Save as JSON
        output_file = "sample_fire_data.json"
        with open(output_file, 'w') as f:
            json.dump(sample_fires, f, indent=2, default=str)
        
        print(f"   ✅ Exported fire data to: {output_file}")
        print(f"   📄 Format: GeoJSON (JSON-based)")
        print(f"   📊 Features: {len(sample_fires.get('features', []))}")
        
        # Show file size
        file_size = os.path.getsize(output_file)
        print(f"   📦 File Size: {file_size:,} bytes")
        
    except Exception as e:
        print(f"   ❌ Error exporting JSON: {str(e)}")
    
    # 5. Show data structure
    print("\n5. 🏗️  DATA STRUCTURE")
    print("-" * 40)
    print("""
   GeoJSON Format:
   {
     "type": "FeatureCollection",
     "features": [
       {
         "type": "Feature",
         "properties": {
           "IncidentName": "Example Fire",
           "POOState": "CA",
           "DailyAcres": 1500,
           "PercentContained": 25,
           "FireDiscoveryDateTime": "2025-07-10T14:30:00Z",
           "StructuresThreated": 45,
           "FireCause": "Lightning",
           ... (50+ additional properties)
         },
         "geometry": {
           "type": "Polygon",
           "coordinates": [[[lon, lat], [lon, lat], ...]]
         }
       }
     ]
   }
    """)
    
    print("\n" + "=" * 60)
    print("🎉 Demo completed!")
    print("\n📋 SUMMARY:")
    print("✅ Live Data: Real-time active fires (updated every 15-30 minutes)")
    print("✅ Historical Data: Multi-year archive of fire perimeters")
    print("✅ JSON Format: GeoJSON standard for web/mapping applications")
    print("✅ Rich Properties: 50+ attributes per fire (size, containment, etc.)")
    print("✅ Geometry Data: Precise fire perimeter polygons")
    print("✅ No API Key Required: Free public data from NIFC/WFIGS")
    print("\n🔧 Perfect for:")
    print("  • Web mapping applications")
    print("  • Historical fire analysis")
    print("  • Real-time monitoring dashboards")
    print("  • Machine learning datasets")
    print("  • Ember transport modeling")


if __name__ == "__main__":
    demo_historical_and_live_data()
