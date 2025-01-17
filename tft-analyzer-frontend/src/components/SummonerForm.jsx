import React, { useState } from 'react';
import axios from 'axios';

const SummonerForm = () => {
  const [region, setRegion] = useState('');
  const [summonerName, setSummonerName] = useState('');
  const [tag, setTag] = useState('');
  const [analysisData, setAnalysisData] = useState(null);
  const [recommendationsData, setRecommendationsData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // Fetch Summoner Analysis
      const analysisResponse = await axios.get(
        `http://127.0.0.1:5000/api/analyze?summoner=${summonerName}&tag=${tag}`
      );

      setAnalysisData(analysisResponse.data);

      // Fetch Recommendations
      const recommendationsResponse = await axios.get(
        `http://127.0.0.1:5000/recommendations`
      );

      setRecommendationsData(recommendationsResponse.data);
    } catch (err) {
      setError('Failed to fetch data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.heading}>TFT Analyzer</h2>
      <p style={styles.description}>Enter your Summoner details to get started!</p>
      <form onSubmit={handleSubmit} style={styles.form}>
        <div style={styles.formGroup}>
          <label style={styles.label}>Region:</label>
          <select
            value={region}
            onChange={(e) => setRegion(e.target.value)}
            style={styles.select}
            required
          >
            <option value="">Select Region</option>
            <option value="NA1">NA1</option>
            <option value="EUW1">EUW1</option>
            <option value="KR">KR</option>
          </select>
        </div>
        <div style={styles.formGroup}>
          <label style={styles.label}>Summoner Name:</label>
          <input
            type="text"
            value={summonerName}
            onChange={(e) => setSummonerName(e.target.value)}
            style={styles.input}
            required
          />
        </div>
        <div style={styles.formGroup}>
          <label style={styles.label}>Tag:</label>
          <input
            type="text"
            value={tag}
            onChange={(e) => setTag(e.target.value)}
            style={styles.input}
            required
          />
        </div>
        <button type="submit" style={styles.button}>
          Analyze
        </button>
      </form>

      {loading && <p>Loading...</p>}
      {error && <p style={styles.error}>{error}</p>}

      {analysisData && (
        <div style={styles.section}>
          <h3>Summoner Analysis</h3>
          <p>Average Placement: {analysisData.average_placement}</p>
          <p>First Place Wins: {analysisData.first_place_wins}</p>
          <p>Total Damage: {analysisData.total_damage}</p>
        </div>
      )}

      {recommendationsData && (
        <div>
          <div style={styles.section}>
            <h3>Top Traits</h3>
            <ul>
              {recommendationsData.trait_recommendations.top_traits.map((trait, index) => (
                <li key={index}>
                  {trait.trait}: Avg Placement = {parseFloat(trait.avg_placement).toFixed(2)}
                </li>
              ))}
            </ul>
          </div>
          <div style={styles.section}>
            <h3>Top Unit Pairs</h3>
            <ul>
              {recommendationsData.unit_recommendations.top_unit_pairs.map((pair, index) => (
                <li key={index}>
                  {pair.unit1} + {pair.unit2}: Avg Placement = {parseFloat(pair.avg_placement).toFixed(2)}
                </li>
              ))}
            </ul>
          </div>
          <div style={styles.section}>
            <h3>Strictly Diverse Combinations</h3>
            <h4>Traits:</h4>
            <ul>
              {recommendationsData.trait_recommendations.strictly_diverse_combinations.map(
                (combo, index) => (
                  <li key={index}>
                    Traits: {combo.traits.join(', ')} | Avg Placement = {parseFloat(combo.avg_placement).toFixed(2)}
                  </li>
                )
              )}
            </ul>
            <h4>Units:</h4>
            <ul>
              {recommendationsData.unit_recommendations.strictly_diverse_combinations.map(
                (combo, index) => (
                  <li key={index}>
                    Units: {combo.units.join(', ')} | Avg Placement = {parseFloat(combo.avg_placement).toFixed(2)}
                  </li>
                )
              )}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

const styles = {
  container: {
    maxWidth: '800px',
    margin: '50px auto',
    padding: '20px',
    border: '1px solid #ddd',
    borderRadius: '8px',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
    backgroundColor: '#f9f9f9',
  },
  heading: {
    textAlign: 'center',
    color: '#333',
    marginBottom: '10px',
  },
  description: {
    textAlign: 'center',
    fontSize: '14px',
    color: '#666',
    marginBottom: '20px',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
  },
  formGroup: {
    marginBottom: '15px',
  },
  label: {
    marginBottom: '5px',
    fontWeight: 'bold',
    display: 'block',
    color: '#555',
  },
  select: {
    width: '100%',
    padding: '10px',
    borderRadius: '4px',
    border: '1px solid #ccc',
  },
  input: {
    width: '100%',
    padding: '10px',
    borderRadius: '4px',
    border: '1px solid #ccc',
  },
  button: {
    width: '100%',
    padding: '10px',
    backgroundColor: '#4caf50',
    color: '#fff',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontWeight: 'bold',
    fontSize: '16px',
  },
  error: {
    color: 'red',
    fontWeight: 'bold',
    textAlign: 'center',
  },
  section: {
    marginTop: '20px',
    padding: '15px',
    backgroundColor: '#fff',
    borderRadius: '8px',
    boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
  },
};

export default SummonerForm;
