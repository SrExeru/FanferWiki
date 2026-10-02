import axios from 'axios';
import { ENV } from '../config/env';

const api = axios.create({
    baseURL: ENV.BACKEND_URL,
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

api.interceptors.response.use(
    response => {
        return response;
    },
    async error => {
        const originalRequest = error.config;

        if (error.response?.status == 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            let refreshedToken = false;
            try {
                response = await axios.get(
                    `${ENV.BACKEND_URL}/auth/refresh`, {
                    withCredentials: true
                });

                const newToken = response.data;

                localStorage.setItem('access_token', newToken);
                
                originalRequest.headers.Authorization = `Bearer ${newToken}`;

                return axios(originalRequest);
            } catch (refreshError) {
                console.error('Refresh error:', refreshError);
                localStorage.removeItem('access_token');
                return Promise.reject(refreshError);
            }
            
        }

        return Promise.reject(error);
    }
)

export default api;