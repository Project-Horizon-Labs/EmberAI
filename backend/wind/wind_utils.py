from backend.wind.wind_service import fetch_open_meteo_wind
from shapely.geometry import shape, mapping
from shapely.errors import ShapelyError
from shapely import affinity
import math


def calculate_wind_zone(fire_perimeter: dict, wind_data: dict) -> dict:
    """
    Calculate a danger zone polygon by buffering the fire perimeter and stretching it along wind direction.
    Args:
        fire_perimeter (dict): GeoJSON polygon of the current fire perimeter.
        wind_data (dict): Dictionary with at least 'speed' and 'direction' keys.

    Returns:
        dict: GeoJSON polygon representing the directional danger zone.
    """
    print(f"Wind speed: {wind_data.get('speed')} m/s, direction: {wind_data.get('direction')} degrees")

    wind_speed = wind_data.get('speed', 0)
    wind_direction = wind_data.get('direction', 0)  # Degrees, 0=north
    scaling_factor = 0.05  # degrees per m/s, much larger for visualization
    buffer_distance = wind_speed * scaling_factor

    # Directional scaling factors
    scale_x = 2.5  # Stretch downwind (major axis)
    scale_y = 1.0  # Perpendicular (minor axis)

    try:
        perimeter_geom = shape(fire_perimeter['geometry'])
        # 1. Buffer
        buffered_geom = perimeter_geom.buffer(buffer_distance)
        # 2. Scale (stretch) the buffer along x (major axis)
        stretched_geom = affinity.scale(buffered_geom, xfact=scale_x, yfact=scale_y, origin='centroid')
        # 3. Rotate to align with wind direction (0 deg=north, shapely rotates ccw from x axis)
        # Convert wind direction to shapely angle: 0=north, 90=east, 180=south, 270=west
        shapely_angle = -wind_direction + 90  # Convert compass to mathematical angle
        rotated_geom = affinity.rotate(stretched_geom, shapely_angle, origin='centroid', use_radians=False)
        # 4. Shift (translate) the geometry downwind to create a teardrop effect
        # Calculate translation distance (e.g., half the buffer distance)
        shift_distance = buffer_distance * scale_x * 0.5
        # Convert wind direction (degrees from north) to radians (mathematical angle)
        theta = math.radians(270 - wind_direction)  # 0° = east, 90° = north
        dx = shift_distance * math.cos(theta)
        dy = shift_distance * math.sin(theta)
        shifted_geom = affinity.translate(rotated_geom, xoff=dx, yoff=dy)
        # 5. Convert back to GeoJSON
        danger_zone_geojson = {
            "type": "Feature",
            "geometry": mapping(shifted_geom),
            "properties": {
                "buffer_distance": buffer_distance,
                "wind_speed": wind_speed,
                "wind_direction": wind_direction,
                "scale_x": scale_x,
                "scale_y": scale_y,
                "shift_distance": shift_distance
            }
        }
        return danger_zone_geojson
    except (KeyError, ShapelyError, TypeError, ValueError) as e:
        print(f"Error creating directional buffer: {e}")
        return fire_perimeter

    