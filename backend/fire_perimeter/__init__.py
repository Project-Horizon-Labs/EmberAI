"""
Fire Perimeter Module for EmberAI
Handles ingestion and processing of fire perimeter data from NIFC/WFIGS APIs
"""

from .fire_perimeter_service import (
    FirePerimeterService,
    AsyncFirePerimeterService,
    FirePerimeterType,
    FirePerimeter
)

__version__ = "1.0.0"
__author__ = "EmberAI Team"

__all__ = [
    "FirePerimeterService",
    "AsyncFirePerimeterService", 
    "FirePerimeterType",
    "FirePerimeter"
]
