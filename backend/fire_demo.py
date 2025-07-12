"""
Example usage of the Fire Perimeter Service for EmberAI
Run this script to test the fire perimeter data ingestion
"""

import json
from fire_perimeter_service import FirePerimeterService, FirePerimeterType


def main():
    """Main function to demonstrate fire perimeter service usage"""
    
    print("🔥 EmberAI Fire Perimeter Service Demo")
    print("=" * 50)
    
    # Initialize the service
    fire_service = FirePerimeterService()
    
    # Example 1: Get current fires nationwide
    print("\n1. Fetching current fires nationwide...")
    try:
        current_fires = fire_service.get_fire_perimeters(
            perimeter_type=FirePerimeterType.CURRENT,
            min_acres=100  # Only fires > 100 acres
        )
        
        fire_count = len(current_fires.get('features', []))
        print(f"   ✅ Found {fire_count} active fires > 100 acres")
        
        if fire_count > 0:
            # Show some details about the largest fire
            largest_fire = max(
                current_fires['features'],
                key=lambda x: x.get('properties', {}).get('DailyAcres', 0)
            )
            
            props = largest_fire.get('properties', {})
            print(f"   🔥 Largest fire: {props.get('IncidentName', 'Unknown')}")
            print(f"      📍 Location: {props.get('POOState', 'Unknown')}")
            print(f"      📏 Size: {props.get('DailyAcres', 0):,} acres")
            print(f"      🚧 Containment: {props.get('PercentContained', 0)}%")
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    # Example 2: Get high-priority fires for ember analysis
    print("\n2. Fetching high-priority fires for ember analysis...")
    try:
        priority_fires = fire_service.get_high_priority_fires(
            min_acres=1000,      # At least 1000 acres
            max_containment=50,   # Less than 50% contained
            structures_threatened=1  # At least 1 structure threatened
        )
        
        priority_count = len(priority_fires.get('features', []))
        print(f"   ✅ Found {priority_count} high-priority fires")
        
        if priority_count > 0:
            print("   🚨 High-priority fires:")
            for feature in priority_fires['features'][:3]:  # Show first 3
                props = feature.get('properties', {})
                name = props.get('IncidentName', 'Unknown')
                state = props.get('POOState', 'Unknown')
                acres = props.get('DailyAcres', 0)
                containment = props.get('PercentContained', 0)
                structures = props.get('StructuresThreated', 0)
                
                print(f"      • {name} ({state}): {acres:,} acres, {containment}% contained, {structures} structures threatened")
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    # Example 3: Get fires near a specific location (Los Angeles)
    print("\n3. Fetching fires near Los Angeles...")
    try:
        la_fires = fire_service.get_fires_by_coordinates(
            latitude=34.0522,   # Los Angeles coordinates
            longitude=-118.2437,
            radius_miles=100    # Within 100 miles
        )
        
        la_count = len(la_fires.get('features', []))
        print(f"   ✅ Found {la_count} fires within 100 miles of Los Angeles")
        
        if la_count > 0:
            print("   🏙️ Fires near Los Angeles:")
            for feature in la_fires['features'][:3]:  # Show first 3
                props = feature.get('properties', {})
                name = props.get('IncidentName', 'Unknown')
                acres = props.get('DailyAcres', 0)
                containment = props.get('PercentContained', 0)
                
                print(f"      • {name}: {acres:,} acres, {containment}% contained")
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    # Example 4: Get fires by state (California)
    print("\n4. Fetching fires in California...")
    try:
        ca_fires = fire_service.get_fire_perimeters(
            perimeter_type=FirePerimeterType.CURRENT,
            state_code="CA",
            min_acres=50
        )
        
        ca_count = len(ca_fires.get('features', []))
        total_acres = sum(f.get('properties', {}).get('DailyAcres', 0) for f in ca_fires.get('features', []))
        
        print(f"   ✅ Found {ca_count} fires in California")
        print(f"   🔥 Total acres burned: {total_acres:,} acres")
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    # Example 5: Parse fire data and create danger zones
    print("\n5. Creating ember danger zone analysis...")
    try:
        # Get fires suitable for ember analysis
        ember_fires = fire_service.get_high_priority_fires(
            min_acres=500,
            max_containment=75
        )
        
        ember_count = len(ember_fires.get('features', []))
        
        if ember_count > 0:
            print(f"   ✅ Analyzing {ember_count} fires for ember transport potential")
            
            # Parse fire features into objects
            fire_objects = fire_service.parse_fire_features(ember_fires)
            
            # Simple danger zone analysis
            danger_zones = []
            for fire in fire_objects:
                # Calculate danger zone radius based on fire size and containment
                base_radius = min(fire.acres / 100, 10)  # Base radius in miles
                containment_multiplier = (100 - fire.containment_percent) / 100
                danger_radius = base_radius * containment_multiplier
                
                danger_zones.append({
                    "fire_name": fire.incident_name,
                    "fire_state": fire.state,
                    "fire_acres": fire.acres,
                    "containment_percent": fire.containment_percent,
                    "danger_zone_radius_miles": round(danger_radius, 2),
                    "ember_risk_level": "HIGH" if danger_radius > 5 else "MEDIUM" if danger_radius > 2 else "LOW",
                    "coordinates": [fire.poi_longitude, fire.poi_latitude]
                })
            
            # Show top 3 highest risk fires
            danger_zones.sort(key=lambda x: x["danger_zone_radius_miles"], reverse=True)
            
            print("   🎯 Top ember risk fires:")
            for zone in danger_zones[:3]:
                print(f"      • {zone['fire_name']} ({zone['fire_state']})")
                print(f"        Risk Level: {zone['ember_risk_level']}")
                print(f"        Danger Zone: {zone['danger_zone_radius_miles']} miles")
                print(f"        Fire Size: {zone['fire_acres']:,} acres")
                print()
            
            # Save the analysis
            saved_path = fire_service.save_fire_data(fire_objects, "ember_risk_analysis.json")
            print(f"   💾 Saved ember risk analysis to: {saved_path}")
        
        else:
            print("   ℹ️  No fires found for ember analysis")
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    # Example 6: API connectivity test
    print("\n6. Testing API connectivity...")
    try:
        # Simple test to verify API is accessible
        test_request = fire_service.get_fire_perimeters(
            perimeter_type=FirePerimeterType.CURRENT
        )
        
        if test_request and 'features' in test_request:
            print("   ✅ API connectivity: OK")
            print(f"   📊 Total active fires: {len(test_request['features'])}")
        else:
            print("   ⚠️  API connectivity: Warning - No data returned")
            
    except Exception as e:
        print(f"   ❌ API connectivity: Failed - {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎉 Demo completed!")
    print("\nNext steps for EmberAI integration:")
    print("1. Set up scheduled data ingestion (every 15-30 minutes)")
    print("2. Integrate with weather data APIs for wind/atmospheric conditions")
    print("3. Implement ember transport modeling algorithms")
    print("4. Create real-time danger zone updates")
    print("5. Connect to drone patrol coordination system")


if __name__ == "__main__":
    main()
