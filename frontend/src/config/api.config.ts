// config/api.config.ts
export const API_CONFIG = {
    BASE_URL: import.meta.env.VITE_API_BASE_URL || 'https://YOUR_API_ENDPOINT/dev',
    USER_ID: import.meta.env.VITE_USER_ID || 'user123', // This should come from auth in production
    ENDPOINTS: {
        CHATS: '/chats',
        CHAT_BY_ID: (chatId: string) => `/chats/${chatId}`,
        CHAT_MESSAGES: (chatId: string) => `/chats/${chatId}/messages`,
    }
};