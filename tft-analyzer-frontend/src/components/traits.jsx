import React, { useState } from 'react';
import { getTopTraits } from '../services/api';

const TraitsAnalysis = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchTopTraits = async () => {
    setLoading(true);
    try {
      const result = await getTopTraits({ top_n: 5 });
      setData(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Top Traits</h2>
      <button onClick={fetchTopTraits}>Get Top Traits</button>
      {loading && <p>Loading...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {data && (
        <ul>
          {data.map((trait, idx) => (
            <li key={idx}>
              {trait.name}: Avg Placement = {trait.avg_placement}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default TraitsAnalysis;
