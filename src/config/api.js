// API Configuration
export const API_BASE_URL = 'http://localhost:5050';

// API Endpoints
export const API_ENDPOINTS = {
  ROOT: '/',
  HEALTH: '/api/health',
  TEST: '/api/test',
};

// Helper function to make API calls
export const apiCall = async (endpoint, options = {}) => {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API call failed:', error);
    throw error;
  }
};

// Example usage:
// import { apiCall, API_ENDPOINTS } from './config/api';
// const data = await apiCall(API_ENDPOINTS.TEST);
