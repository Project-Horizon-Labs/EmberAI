import React, { useState } from 'react';
import { MapContainer, TileLayer, GeoJSON } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const sampleGeoJson = {
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [-98, -39]
      },
      "properties": {
        "name": "Center of the United States"
      }
    }
  ]
};

const geoJsonStyle = {
  color: 'red',
  weight: 2,
  fillColor: 'red',
  fillOpacity: 0.3,
};

const TILE_LAYERS = [
  {
    key: 'satellite',
    url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
    label: 'Satellite',
    button: 'Switch to Dark Mode',
  },
  {
    key: 'dark',
    url: 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
    attribution: '&copy; <a href="https://carto.com/attributions">CARTO</a> | &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    label: 'Dark Mode',
    button: 'Switch to OpenStreetMap',
  },
  {
    key: 'osm',
    url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    attribution: '&copy; OpenStreetMap contributors',
    label: 'OpenStreetMap',
    button: 'Switch to Satellite',
  },
];

const MapView = ({ geoJson = sampleGeoJson }) => {
  const [layerIndex, setLayerIndex] = useState(0);

  const handleToggle = () => {
    setLayerIndex((prev) => (prev + 1) % TILE_LAYERS.length);
  };

  const { url, attribution, button } = TILE_LAYERS[layerIndex];

  return (
    <div style={{ position: 'relative' }}>
      <button
        onClick={handleToggle}
        style={{
          position: 'absolute',
          zIndex: 1000,
          top: 10,
          right: 10,
          background: '#222',
          color: '#fff',
          border: 'none',
          borderRadius: 8,
          padding: '8px 16px',
          fontWeight: 600,
          cursor: 'pointer',
          opacity: 0.85,
        }}
      >
        {button}
      </button>
      <MapContainer center={[39.8283, -98.5795]} zoom={4} style={{ height: '60vh', width: '100%' }}>
        <TileLayer attribution={attribution} url={url} />
        <GeoJSON data={geoJson} style={geoJsonStyle} />
      </MapContainer>
    </div>
  );
};

export default MapView;
