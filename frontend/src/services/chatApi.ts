// services/chatApi.ts
import { API_CONFIG } from '../config/api.config';
import type {
    GetChatsResponse,
    GetChatResponse,
    CreateChatResponse,
    AppendMessageResponse,
    DeleteChatResponse,
    ApiChatSession,
    ApiChatDetail,
    ChatSession,
    Message,
} from '../types/chat.types';

// Helper function to convert API chat session to UI format
const convertApiChatToUi = (apiChat: ApiChatSession): ChatSession => {
    return {
        id: apiChat.chat_id,
        title: apiChat.title,
        lastMessage: '', // We'll need to fetch full chat to get this
        timestamp: new Date(apiChat.created_at),
        messageCount: apiChat.message_count,
        updatedAt: new Date(apiChat.updated_at),
    };
};

// Helper function to convert API messages to UI format
const convertApiMessagesToUi = (apiMessages: ApiChatDetail['messages']): Message[] => {
    return apiMessages.map((msg, index) => ({
        id: Date.now() + index,
        text: msg.content,
        sender: msg.role === 'user' ? 'user' : 'bot',
        timestamp: new Date(msg.timestamp),
        role: msg.role,
        content: msg.content,
    }));
};

/**
 * Get all chats for the current user, sorted by most recently updated
 */
export const getChatSessions = async (): Promise<ChatSession[]> => {
    try {
        const url = `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.CHATS}?user_id=${API_CONFIG.USER_ID}`;

        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error(`Failed to fetch chat sessions: ${response.statusText}`);
        }

        const data: GetChatsResponse = await response.json();

        // Convert API format to UI format and sort by updated_at (most recent first)
        const sessions = data.chats
            .map(convertApiChatToUi)
            .sort((a, b) => b.updatedAt.getTime() - a.updatedAt.getTime());

        return sessions;
    } catch (error) {
        console.error('Error fetching chat sessions:', error);
        throw error;
    }
};

/**
 * Get a specific chat by ID with all its messages
 */
export const getChatById = async (chatId: string): Promise<{ id: string; messages: Message[] }> => {
    try {
        const url = `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.CHAT_BY_ID(chatId)}`;

        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error(`Failed to fetch chat: ${response.statusText}`);
        }

        const data: GetChatResponse = await response.json();

        return {
            id: data.chat.chat_id,
            messages: convertApiMessagesToUi(data.chat.messages),
        };
    } catch (error) {
        console.error('Error fetching chat:', error);
        throw error;
    }
};

/**
 * Create a new chat with the first message
 */
export const createChat = async (
    message: string,
    metadata?: Record<string, any>
): Promise<CreateChatResponse> => {
    try {
        const url = `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.CHATS}`;

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: API_CONFIG.USER_ID,
                message,
                role: 'user',
                metadata: metadata || { source: 'web' },
            }),
        });

        if (!response.ok) {
            throw new Error(`Failed to create chat: ${response.statusText}`);
        }

        const data: CreateChatResponse = await response.json();
        return data;
    } catch (error) {
        console.error('Error creating chat:', error);
        throw error;
    }
};

/**
 * Append a message to an existing chat
 */
export const appendMessage = async (
    chatId: string,
    message: string,
    role: 'user' | 'assistant' = 'user'
): Promise<AppendMessageResponse> => {
    try {
        const url = `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.CHAT_MESSAGES(chatId)}`;

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message,
                role,
            }),
        });

        if (!response.ok) {
            throw new Error(`Failed to append message: ${response.statusText}`);
        }

        const data: AppendMessageResponse = await response.json();
        return data;
    } catch (error) {
        console.error('Error appending message:', error);
        throw error;
    }
};

/**
 * Delete a chat by ID
 */
export const deleteChat = async (chatId: string): Promise<void> => {
    try {
        const url = `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.CHAT_BY_ID(chatId)}`;

        const response = await fetch(url, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error(`Failed to delete chat: ${response.statusText}`);
        }

        const data: DeleteChatResponse = await response.json();
        console.log(data.message);
    } catch (error) {
        console.error('Error deleting chat:', error);
        throw error;
    }
};

/**
 * Send a message and get AI response
 * This is a placeholder - you'll need to implement based on how your AI responds
 */
export const sendMessage = async (message: string): Promise<string> => {
    try {
        // TODO: Implement AI response endpoint
        // This might be a separate endpoint or part of the append message response

        // For now, return a placeholder
        // You'll need to update this based on your actual AI integration
        await new Promise(resolve => setTimeout(resolve, 1000));
        return `AI Response to: ${message}`;
    } catch (error) {
        console.error('Error sending message:', error);
        throw error;
    }
};