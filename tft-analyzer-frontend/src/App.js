import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import SummonerAnalysis from './components/summoner';
import TraitsAnalysis from './components/traits';
import Recommendations from './components/recommendations';

const App = () => {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li>
              <Link to="/">Home</Link>
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
          <Route path="/" element={<h1>Welcome to TFT Analyzer</h1>} />
          <Route path="/summoner" element={<SummonerAnalysis />} />
          <Route path="/traits" element={<TraitsAnalysis />} />
          <Route path="/recommendations" element={<Recommendations />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
