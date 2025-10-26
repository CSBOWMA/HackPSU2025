// src/config/api.config.ts
export const API_CONFIG = {
    BASE_URL: import.meta.env.VITE_API_BASE_URL,
    USER_ID: import.meta.env.VITE_USER_ID,
    FASTAPI_BASE_URL: import.meta.env.VITE_FASTAPI_BASE_URL || 'http://localhost:8000',
    ENDPOINTS: {
        CHATS: '/chats',
        CHAT_BY_ID: (chatId: string) => `/chats/${chatId}`,
        CHAT_MESSAGES: (chatId: string) => `/chats/${chatId}/messages`,
        RAG_QUERY: '/query-rag',
    },
} as const;

// Debug logging (remove in production)
console.log('API Config:', {
    BASE_URL: API_CONFIG.BASE_URL,
    FASTAPI_BASE_URL: API_CONFIG.FASTAPI_BASE_URL,
    USER_ID: API_CONFIG.USER_ID,
});