import React from 'react';
import MapView from './MapView';
import styles from './Toolskit.module.css';

const Toolskit = () => (
  <div className={styles['toolskit-page']}>
    <h1>Toolskit</h1>
    <p>This is where the main functionality will be implemented, including the map and GeoJSON support.</p>
    <MapView />
  </div>
);

export default Toolskit;
