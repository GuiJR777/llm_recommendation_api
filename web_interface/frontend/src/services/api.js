
import axios from 'axios';

const API_BASE = 'http://localhost:8000/api';
const LLM_API_BASE = 'http://localhost:8000'; // principal

export const getAllUsers = () => axios.get(`${API_BASE}/users`).then(res => res.data);
export const getUserById = (id) => axios.get(`${API_BASE}/users/${id}`).then(res => res.data);
export const getAllProducts = () => axios.get(`${API_BASE}/products`).then(res => res.data);
export const getProductById = (id) => axios.get(`${API_BASE}/products/${id}`).then(res => res.data);
export const getRecommendations = (userId) => axios.get(`${LLM_API_BASE}/user-recommendations/${userId}`).then(res => res.data.recommendations);
export const getProductDescription = (productId, userId = null) =>
  axios.get(`${LLM_API_BASE}/product-description/${productId}`, { params: { user_id: userId } }).then(res => res.data.personalized_description);
