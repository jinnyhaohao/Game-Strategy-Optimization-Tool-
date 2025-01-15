import React, { useState } from 'react';
import { analyzeSummoner } from '../services/api';

const SummonerAnalysis = () => {
  const [summoner, setSummoner] = useState('');
  const [tag, setTag] = useState('');
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchSummonerData = async () => {
    setLoading(true);
    try {
      const result = await analyzeSummoner(summoner, tag);
      setData(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Summoner Analysis</h2>
      <input
        type="text"
        placeholder="Summoner Name"
        value={summoner}
        onChange={(e) => setSummoner(e.target.value)}
      />
      <input
        type="text"
        placeholder="Tag"
        value={tag}
        onChange={(e) => setTag(e.target.value)}
      />
      <button onClick={fetchSummonerData}>Analyze</button>
      {loading && <p>Loading...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {data && (
        <div>
          <p>Average Placement: {data.average_placement}</p>
          <p>First Place Wins: {data.first_place_wins}</p>
          <p>Total Damage: {data.total_damage}</p>
        </div>
      )}
    </div>
  );
};

export default SummonerAnalysis;
