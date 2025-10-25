// services/chatApi.ts
import type { ChatApiRequest, ChatApiResponse, ChatSession, SaveChatRequest } from '../types/chat.types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000/api';

// Simulate API delay for development
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

// Temporary in-memory storage (will be replaced with actual API calls)
let chatSessionsStorage: ChatSession[] = [];
let chatMessagesStorage: Record<string, any[]> = {};

export const sendMessage = async (message: string): Promise<string> => {
    try {
        // TODO: Replace with actual API call
        // const response = await fetch(`${API_BASE_URL}/chat`, {
        //     method: 'POST',
        //     headers: {
        //         'Content-Type': 'application/json',
        //     },
        //     body: JSON.stringify({ message } as ChatApiRequest),
        // });

        // if (!response.ok) {
        //     throw new Error('Failed to send message');
        // }

        // const data: ChatApiResponse = await response.json();
        // return data.message;

        // Simulated response for development
        await delay(1000);
        return `Echo: ${message}`;
    } catch (error) {
        console.error('Error sending message:', error);
        throw error;
    }
};

export const getChatSessions = async (): Promise<ChatSession[]> => {
    try {
        // TODO: Replace with actual API call
        // const response = await fetch(`${API_BASE_URL}/chats`, {
        //     method: 'GET',
        //     headers: {
        //         'Content-Type': 'application/json',
        //     },
        // });

        // if (!response.ok) {
        //     throw new Error('Failed to fetch chat sessions');
        // }

        // const data: ChatSessionsResponse = await response.json();
        // return data.sessions;

        // Simulated response for development
        await delay(500);
        return chatSessionsStorage;
    } catch (error) {
        console.error('Error fetching chat sessions:', error);
        throw error;
    }
};

export const getChatById = async (chatId: string): Promise<any> => {
    try {
        // TODO: Replace with actual API call
        // const response = await fetch(`${API_BASE_URL}/chats/${chatId}`, {
        //     method: 'GET',
        //     headers: {
        //         'Content-Type': 'application/json',
        //     },
        // });

        // if (!response.ok) {
        //     throw new Error('Failed to fetch chat');
        // }

        // return await response.json();

        // Simulated response for development
        await delay(500);
        return {
            id: chatId,
            messages: chatMessagesStorage[chatId] || []
        };
    } catch (error) {
        console.error('Error fetching chat:', error);
        throw error;
    }
};

export const saveChat = async (chatData: SaveChatRequest): Promise<void> => {
    try {
        // TODO: Replace with actual API call
        // const response = await fetch(`${API_BASE_URL}/chats/${chatData.chatId}`, {
        //     method: 'PUT',
        //     headers: {
        //         'Content-Type': 'application/json',
        //     },
        //     body: JSON.stringify(chatData),
        // });

        // if (!response.ok) {
        //     throw new Error('Failed to save chat');
        // }

        // Simulated save for development
        await delay(300);

        chatMessagesStorage[chatData.chatId] = chatData.messages;

        const existingSessionIndex = chatSessionsStorage.findIndex(s => s.id === chatData.chatId);

        const lastMessage = chatData.messages.length > 0
            ? chatData.messages[chatData.messages.length - 1].text
            : 'New chat';

        const title = chatData.title || (chatData.messages.length > 0
            ? chatData.messages[0].text.slice(0, 50)
            : 'New Chat');

        const sessionData: ChatSession = {
            id: chatData.chatId,
            title,
            lastMessage,
            timestamp: new Date(),
            messageCount: chatData.messages.length
        };

        if (existingSessionIndex >= 0) {
            chatSessionsStorage[existingSessionIndex] = sessionData;
        } else {
            chatSessionsStorage = [sessionData, ...chatSessionsStorage];
        }
    } catch (error) {
        console.error('Error saving chat:', error);
        throw error;
    }
};

export const deleteChat = async (chatId: string): Promise<void> => {
    try {
        // TODO: Replace with actual API call
        // const response = await fetch(`${API_BASE_URL}/chats/${chatId}`, {
        //     method: 'DELETE',
        //     headers: {
        //         'Content-Type': 'application/json',
        //     },
        // });

        // if (!response.ok) {
        //     throw new Error('Failed to delete chat');
        // }

        // Simulated delete for development
        await delay(300);
        chatSessionsStorage = chatSessionsStorage.filter(s => s.id !== chatId);
        delete chatMessagesStorage[chatId];
    } catch (error) {
        console.error('Error deleting chat:', error);
        throw error;
    }
};