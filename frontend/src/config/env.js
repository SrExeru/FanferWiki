export const ENV = {
    BACKEND_URL: import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'
}

Object.freeze(ENV);