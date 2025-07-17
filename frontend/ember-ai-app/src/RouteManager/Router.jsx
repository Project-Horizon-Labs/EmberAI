import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import navStyles from './NavTabs.module.css';
import Home from '../Home/Home';
import Toolskit from '../Components/Toolskit';

function NavTabs() {
  const location = useLocation();
  return (
    <nav className={navStyles.nav}>
      <Link
        to="/"
        className={location.pathname === '/' ? `${navStyles.tab} ${navStyles.active}` : navStyles.tab}
      >
        Home/About
      </Link>
      <Link
        to="/toolskit"
        className={location.pathname === '/toolskit' ? `${navStyles.tab} ${navStyles.active}` : navStyles.tab}
      >
        Toolskit
      </Link>
    </nav>
  );
}

const AppRouter = () => (
  <Router>
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      <NavTabs />
      <main style={{ flex: 1, marginLeft: 180, width: '100vw', height: '100vh', overflow: 'hidden' }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/toolskit" element={<Toolskit />} />
        </Routes>
      </main>
    </div>
  </Router>
);

export default AppRouter;
