import axios from 'axios';

const API_BASE = 'http://localhost:3001/api'; // backend BFF
const LLM_API_BASE = 'http://localhost:8000'; // API principal (LLM + recomendação)

export const getAllUsers = () => axios.get(`${API_BASE}/users`).then(res => res.data);
export const getUserById = (id) => axios.get(`${API_BASE}/users/${id}`).then(res => res.data);
export const getAllProducts = () => axios.get(`${API_BASE}/products`).then(res => res.data);
export const getProductById = (id) => axios.get(`${API_BASE}/products/${id}`).then(res => res.data);

export const getRecommendations = (userId, strategy = "history") =>
  axios.get(`${LLM_API_BASE}/user-recommendations/${userId}`, {
    params: { strategy }
  }).then(res => res.data);

export const getProductDescription = (productId, userId = null, llm = "emulator") =>
  axios.get(`${LLM_API_BASE}/product-description/${productId}`, {
    params: {
      user_id: userId,
      llm: llm
    }
  }).then(res => res.data.personalized_description);
