import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json'
    }
});

// Add JWT token to requests automatically
api.interceptors.request.use(config => {
    const token = localStorage.getItem('access_token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Handle errors (e.g., unauthorized)
api.interceptors.response.use(
    response => response,
    error => {
        if (error.response?.status === 401) {
            // Token expired, clear it
            localStorage.removeItem('access_token');
            window.location.href = '/';
        }
        return Promise.reject(error);
    }
);

// Authentication functions
export const auth = {
    register: (email, password) =>
        api.post('/auth/register', { email, password }),
    login: (email, password) =>
        api.post('/auth/login', { email, password })
};

// Farm functions
export const farms = {
    create: (name, location, crop_type) =>
        api.post('/farms', { name, location, crop_type }),
    list: () => api.get('/farms'),
    get: (farm_id) => api.get(`/farms/${farm_id}`),
    getData: (farm_id, days = 7) =>
        api.get(`/farms/${farm_id}/data?days=${days}`),
    getLatest: (farm_id) =>
        api.get(`/farms/${farm_id}/latest`),
    getAlerts: (farm_id) =>
        api.get(`/farms/${farm_id}/alerts`)
};

// Sensor functions
export const sensor = {
    submit: (farm_id, temperature, humidity, soil_moisture, light_intensity = null) =>
        api.post('/sensor-data', {
            farm_id,
            temperature,
            humidity,
            soil_moisture,
            light_intensity
        })
};

export default api;