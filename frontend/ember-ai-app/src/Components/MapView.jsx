import React from 'react';
import { MapContainer, TileLayer, GeoJSON } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const sampleGeoJson = {
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [-98.5795, 39.8283] // Center of US
      },
      "properties": {
        "name": "Center of the United States"
      }
    }
  ]
};

const MapView = ({ geoJson = sampleGeoJson }) => (
  <MapContainer center={[39.8283, -98.5795]} zoom={4} style={{ height: '60vh', width: '100%' }}>
    <TileLayer
      attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
    />
    <GeoJSON data={geoJson} />
  </MapContainer>
);

export default MapView;
