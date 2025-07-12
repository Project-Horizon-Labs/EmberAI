"""
Simple test to verify fire perimeter data is working
"""
from fire_perimeter import FirePerimeterService, FirePerimeterType
import json

# Test current fires
fs = FirePerimeterService()

print("Testing current fires (no filters)...")
result = fs.get_fire_perimeters(FirePerimeterType.CURRENT)
print(f"Found {len(result.get('features', []))} total current fires")
print(f"Data type: {type(result)}")

if result.get('features'):
    sample = result['features'][0]
    print(f"Sample fire: {sample.get('properties', {}).get('IncidentName', 'Unknown')}")
    print(f"Sample acres: {sample.get('properties', {}).get('DailyAcres', 0)}")

# Test historical data
print("\nTesting historical fires (no filters)...")
hist_result = fs.get_fire_perimeters(FirePerimeterType.HISTORICAL)
print(f"Found {len(hist_result.get('features', []))} historical fires")

# Export sample
with open('test_export.json', 'w') as f:
    json.dump(result, f, indent=2, default=str)
print("Exported sample to test_export.json")
