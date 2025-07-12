# Fire Perimeter Data Directory

This directory stores cached fire perimeter data and analysis results from the EmberAI fire perimeter service.

## Files

- `fire_perimeters_*.json` - Cached fire perimeter data with timestamps
- `ember_risk_analysis.json` - Ember risk analysis results
- `danger_zones_*.json` - Generated danger zone data

## Data Sources

The fire perimeter service fetches data from:
- **NIFC/WFIGS**: National Interagency Fire Center / Wildland Fire Information and Geographic Support
- **Current Fires**: Real-time active fire perimeters
- **Historical Fires**: Historical fire perimeter data by decade
- **Certified Fires**: Officially certified fire perimeter data

## Data Retention

- Current fire data: Updated every 15-30 minutes
- Historical analysis: Updated daily
- Cached data: Retained for 7 days (configurable)

## Usage

The data in this directory is used by the EmberAI system for:
1. Ember transport modeling
2. Danger zone calculation
3. Drone patrol planning
4. Historical fire pattern analysis
