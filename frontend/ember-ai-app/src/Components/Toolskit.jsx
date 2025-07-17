import React, { useEffect, useState } from 'react';
import MapView from './MapView';
import styles from './Toolskit.module.css';

const Toolskit = () => {
  const [geoJson, setGeoJson] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Bounding box for the contiguous United States (approx): xmin, ymin, xmax, ymax
  // Longitude: -125 to -66, Latitude: 24 to 50
  const usBbox = '-125,24,-66,50';

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/api/fires/live/current?bbox=${usBbox}`)
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch live fire data');
        return res.json();
      })
      .then(data => setGeoJson(data))
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className={styles['toolskit-page']}>
      <h1>Toolskit</h1>
      <p>This is where the main functionality will be implemented, including the map and GeoJSON support.</p>
      {loading && <div>Loading live fire data...</div>}
      {error && <div style={{ color: 'red' }}>Error: {error}</div>}
      {geoJson && <MapView geoJson={geoJson} />}
    </div>
  );
};

export default Toolskit;
