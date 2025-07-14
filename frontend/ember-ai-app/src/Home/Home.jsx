import React from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './Home.module.css';

const Home = () => {
  const navigate = useNavigate();
  return (
    <div className={styles['home-page']}>
      <div className={styles['accent-bar']} />
      <div className={styles['home-card']}>
        <h1>Welcome to EmberAI</h1>
        <p>EmberAI is your modern toolkit for exploring, visualizing, and working with geospatial data in the United States and beyond.</p>
        <ul style={{ paddingLeft: '1.2em', margin: '0 0 1.2em 0', color: '#3b3b3b', fontSize: '1.08em' }}>
          <li>🌎 Interactive, beautiful world & US maps</li>
          <li>📂 Effortless GeoJSON file support</li>
          <li>🛠️ Powerful toolkit for spatial analysis</li>
          <li>✨ Fast, modern, and easy to use</li>
        </ul>
        <button className={styles['get-started-btn']} onClick={() => navigate('/toolskit')}>
          Get Started
        </button>
      </div>
    </div>
  );
};

export default Home;
