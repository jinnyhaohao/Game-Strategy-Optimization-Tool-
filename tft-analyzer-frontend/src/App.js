import React from 'react';
import SummonerAnalysis from './components/summoner';
import TraitsAnalysis from './components/traits';
import Recommendations from './components/recommendations';
import './App.css';

import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import SummonerForm from './components/SummonerForm'; // Import your form component

const App = () => {
  return (
    <Router>
      <div style={{ padding: '20px' }}>
        <h1>TFT Analyzer</h1>
        <nav>
          <ul>
            <li>
              <Link to="/">Summoner Form</Link>
            </li>
            <li>
              <Link to="/summoner">Summoner Analysis</Link>
            </li>
            <li>
              <Link to="/traits">Top Traits</Link>
            </li>
            <li>
              <Link to="/recommendations">Recommendations</Link>
            </li>
          </ul>
        </nav>

        <Routes>
          <Route path="/" element={<SummonerForm />} />
          <Route path="/summoner" element={<SummonerAnalysis />} />
          <Route path="/traits" element={<TraitsAnalysis />} />
          <Route path="/recommendations" element={<Recommendations />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
