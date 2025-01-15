import React, { useState } from 'react';
import { getRecommendations } from '../services/api';

const Recommendations = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchRecommendations = async () => {
    setLoading(true);
    try {
      const result = await getRecommendations({ top_n: 5, combo_size: 3 });
      setData(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Recommendations</h2>
      <button onClick={fetchRecommendations}>Get Recommendations</button>
      {loading && <p>Loading...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {data && (
        <div>
          <h3>Top Unit Pairs:</h3>
          <ul>
            {data.top_unit_pairs.map((pair, idx) => (
              <li key={idx}>
                {pair.unit1} + {pair.unit2}: Avg Placement = {pair.avg_placement}
              </li>
            ))}
          </ul>

          <h3>Strictly Diverse Combinations:</h3>
          <ul>
            {data.strictly_diverse_combinations.map((combo, idx) => (
              <li key={idx}>
                {combo.units.join(', ')}: Avg Placement = {combo.avg_placement}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default Recommendations;
