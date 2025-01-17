import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const SummonerForm = ({ setSummonerData }) => {
  const [summonerName, setSummonerName] = useState('');
  const [region, setRegion] = useState('');
  const [tag, setTag] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!summonerName || !region || !tag) {
      alert('Please fill in all fields.');
      return;
    }

    // Call backend API for summoner analysis
    try {
      const response = await fetch(
        `http://localhost:5000/api/analyze?summoner=${summonerName}&tag=${tag}&region=${region}`
      );
      const data = await response.json();
      if (data.error) throw new Error(data.error);

      setSummonerData(data);
      navigate('/results');
    } catch (error) {
      alert(`Error: ${error.message}`);
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: 'auto', textAlign: 'center', padding: '20px' }}>
      <h1>TFT Analyzer</h1>
      <p>Analyze your performance and get top recommendations for Teamfight Tactics.</p>
      <form onSubmit={handleSubmit} style={{ marginTop: '20px' }}>
        <input
          type="text"
          placeholder="Enter Summoner Name"
          value={summonerName}
          onChange={(e) => setSummonerName(e.target.value)}
          style={{
            padding: '10px',
            width: '100%',
            marginBottom: '10px',
            borderRadius: '5px',
            border: '1px solid #ccc',
          }}
        />
        <input
          type="text"
          placeholder="Enter Tag (e.g., NA1)"
          value={tag}
          onChange={(e) => setTag(e.target.value)}
          style={{
            padding: '10px',
            width: '100%',
            marginBottom: '10px',
            borderRadius: '5px',
            border: '1px solid #ccc',
          }}
        />
        <select
          value={region}
          onChange={(e) => setRegion(e.target.value)}
          style={{
            padding: '10px',
            width: '100%',
            marginBottom: '20px',
            borderRadius: '5px',
            border: '1px solid #ccc',
          }}
        >
          <option value="">Select Region</option>
          <option value="NA1">North America</option>
          <option value="EUW1">Europe West</option>
          <option value="KR">Korea</option>
          {/* Add more regions as needed */}
        </select>
        <button
          type="submit"
          style={{
            padding: '10px 20px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
          }}
        >
          Analyze
        </button>
      </form>
    </div>
  );
};

export default SummonerForm;
