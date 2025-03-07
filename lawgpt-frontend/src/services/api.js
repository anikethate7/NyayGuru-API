import axios from "axios";

const API_URL = "/api";

const api = {
  // Create a new chat session
  createSession: async () => {
    const response = await axios.post(`${API_URL}/chat/session`);
    return response.data;
  },

  // Fetch all available legal categories
  fetchCategories: async () => {
    const response = await axios.get(`${API_URL}/categories/`);
    return response.data;
  },

  // Fetch all supported languages
  fetchLanguages: async () => {
    const response = await axios.get(`${API_URL}/categories/languages`);
    return response.data;
  },

  // Send a chat message
  sendMessage: async (query, category, language, sessionId) => {
    const response = await axios.post(`${API_URL}/chat/category/${category}`, {
      query,
      category,
      language,
      session_id: sessionId,
    });
    return response.data;
  },
};

export default api;
