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
    error => {
        if (error.response && error.response.status == 401) {
            let refreshedToken = false;
            try {
                axios.get(`${ENV.BACKEND_URL}/auth/refresh`)
                    .then(response => {
                        localStorage.setItem('access_token', response.data);
                        refreshedToken = true;
                    });
                
                    if (!refreshedToken) {
                        return error;
                    }

                    const originalRequest = error.config;
                    originalRequest.headers.Authorization = `Bearer ${access_token}`;

                    return axios(originalRequest);
            } catch (refreshError) {
                console.error('Refresh error:', refreshError);
                return Promise.reject(refreshError);
            }
            
        }

        return Promise.reject(refreshError);
    }
)

export default api;