import axios from 'axios';

const api = axios.create({
    baseURL: import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000',
    timeout: 5000,
});

api.interceptors.request.use(
    config => {
        const access_token = localStorage.getItem('access_token');

        if (access_token) {
            config.headers.Authorization = `Bearer ${access_token}`;
        }

        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

export default api;