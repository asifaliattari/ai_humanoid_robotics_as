/**
 * API Configuration
 * Sets the backend URL based on environment
 */

// Check if we're in production without a backend
const isDevelopment = typeof window !== 'undefined' && window.location.hostname === 'localhost';

// Backend API base URL - Hugging Face Spaces
const PRODUCTION_BACKEND_URL = 'https://asifaliastolixgen-physical-ai-book-api.hf.space';

export const API_BASE_URL = isDevelopment
  ? 'http://localhost:8000'
  : PRODUCTION_BACKEND_URL;

// Flag to check if backend is configured
export const IS_BACKEND_AVAILABLE = isDevelopment || PRODUCTION_BACKEND_URL !== '';

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
