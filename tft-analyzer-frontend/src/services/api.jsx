import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:5000';

export const getRecommendations = async (params) => {
  const response = await axios.get(`${API_BASE_URL}/recommendations`, { params });
  return response.data;
};

export const analyzeSummoner = async (summoner, tag) => {
  const response = await axios.get(`${API_BASE_URL}/api/analyze`, {
    params: { summoner, tag },
  });
  return response.data;
};

export const getTopTraits = async (params) => {
  const response = await axios.get(`${API_BASE_URL}/recommendations/traits`, { params });
  return response.data;
};
