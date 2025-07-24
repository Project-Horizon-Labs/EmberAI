from backend.wind.wind_utils import calculate_wind_zone
import json

# Example fire perimeter (GeoJSON Polygon)
fire_perimeter = {
    "type": "Feature",
    "geometry": {
        "type": "Polygon",
        "coordinates": [[
            [-120.0, 38.0],
            [-121.0, 38.0],
            [-121.0, 39.0],
            [-120.0, 39.0],
            [-120.0, 38.0]
        ]]
    },
    "properties": {}
}

# Example wind data
wind_data = {
    "speed": 8,         # meters/second
    "direction": 270    # degrees (west)
}

danger_zone = calculate_wind_zone(fire_perimeter, wind_data)

from shapely.geometry import shape
import math

# Generate wind arrow (LineString) from centroid in wind direction
perimeter_geom = shape(fire_perimeter["geometry"])
centroid = perimeter_geom.centroid
arrow_length = 0.2  # degrees, much larger for visibility
wind_angle_rad = math.radians(270 - wind_data["direction"])  # 0=east, 90=north
arrow_end = [
    centroid.x + arrow_length * math.cos(wind_angle_rad),
    centroid.y + arrow_length * math.sin(wind_angle_rad)
]
wind_arrow = {
    "type": "Feature",
    "geometry": {
        "type": "LineString",
        "coordinates": [ [centroid.x, centroid.y], arrow_end ]
    },
    "properties": {
        "speed": wind_data["speed"],
        "direction": wind_data["direction"],
        "label": f"{wind_data['speed']} m/s"
    }
}
# Add a Point for the label
wind_label = {
    "type": "Feature",
    "geometry": {
        "type": "Point",
        "coordinates": [centroid.x, centroid.y]
    },
    "properties": {
        "label": f"{wind_data['speed']} m/s, {wind_data['direction']}°"
    }
}

# Output all as a FeatureCollection
feature_collection = {
    "type": "FeatureCollection",
    "features": [fire_perimeter, wind_arrow, wind_label, danger_zone]
}

with open("danger_zone_combined.geojson", "w") as f:
    json.dump(feature_collection, f, indent=2)

print("FeatureCollection with perimeter, wind arrow, label, and danger zone saved to danger_zone_combined.geojson. You can visualize it at https://geojson.io/")
