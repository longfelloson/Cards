import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);

api.interceptors.response.use(
  response => response,
  error => {
    const isLoginPage = window.location.pathname === "/login"
    if (error.response?.status === 401 && !isLoginPage) {
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
