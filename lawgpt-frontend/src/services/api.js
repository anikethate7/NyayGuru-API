// Updated API service to include authentication endpoints
import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:3001/api";

// Create an axios instance with default config
const axiosInstance = axios.create({
  baseURL: API_URL,
  timeout: 30000, // 30 seconds
  headers: {
    "Content-Type": "application/json",
  },
});

// Add a request interceptor to add the auth token to requests
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("authToken");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add a response interceptor to handle auth errors
axiosInstance.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response && error.response.status === 401) {
      // Unauthorized - clear token and redirect to login
      localStorage.removeItem("authToken");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

const api = {
  // Existing methods
  initSession: async () => {
    try {
      const response = await axiosInstance.get("/session/init");
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  sendMessage: async (message, category, language, sessionId) => {
    try {
      const response = await axiosInstance.post("/chat/message", {
        message,
        category,
        language,
        sessionId,
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // New authentication methods
  signup: async (userData) => {
    try {
      const response = await axiosInstance.post("/auth/signup", userData);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  login: async (email, password) => {
    try {
      const response = await axiosInstance.post("/auth/login", {
        email,
        password,
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  logout: async () => {
    try {
      await axiosInstance.post("/auth/logout");
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  validateToken: async (token) => {
    try {
      const response = await axiosInstance.get("/auth/validate", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  resetPassword: async (email) => {
    try {
      const response = await axiosInstance.post("/auth/reset-password", {
        email,
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  updatePassword: async (token, newPassword) => {
    try {
      const response = await axiosInstance.post("/auth/update-password", {
        token,
        newPassword,
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },
};

export default api;
