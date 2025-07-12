"""
Example of integrating fire_perimeter module with main EmberAI backend
"""

from fire_perimeter import FirePerimeterService, FirePerimeterType

def integrate_fire_data():
    """Example function showing how to integrate fire perimeter data"""
    
    # Initialize the fire service
    fire_service = FirePerimeterService()
    
    # Get current high-priority fires
    priority_fires = fire_service.get_high_priority_fires(
        min_acres=1000,
        max_containment=50
    )
    
    print(f"Found {len(priority_fires.get('features', []))} high-priority fires")
    
    # This data can now be used for:
    # 1. Ember transport modeling
    # 2. Drone patrol planning
    # 3. Weather data integration
    # 4. Real-time alerts
    
    return priority_fires

if __name__ == "__main__":
    integrate_fire_data()
