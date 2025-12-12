/**
 * API Configuration
 * Sets the backend URL based on environment
 */

// Backend API base URL
export const API_BASE_URL =
  process.env.NODE_ENV === 'production'
    ? 'https://your-backend.run.app' // Change this when you deploy
    : 'http://localhost:8000';

// API endpoints
export const API_ENDPOINTS = {
  // Health
  health: `${API_BASE_URL}/health`,

  // Authentication
  register: `${API_BASE_URL}/api/auth/register`,
  login: `${API_BASE_URL}/api/auth/login-json`,
  me: `${API_BASE_URL}/api/auth/me`,

  // RAG
  bookQA: `${API_BASE_URL}/api/rag/book-qa`,
  selectionQA: `${API_BASE_URL}/api/rag/selection-qa`,

  // Translation
  translate: `${API_BASE_URL}/api/translation/translate`,
  supportedLanguages: `${API_BASE_URL}/api/translation/supported-languages`,

  // Personalization
  profile: `${API_BASE_URL}/api/personalization/profile`,
  adaptContent: `${API_BASE_URL}/api/personalization/adapt-content`,
  previewAdaptations: `${API_BASE_URL}/api/personalization/preview`,
};

export default API_BASE_URL;
