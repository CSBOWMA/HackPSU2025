// types/chat.types.ts

export interface ChatApiResponse {
    message: string;
}

export interface ChatApiRequest {
    message: string;
}

export interface UseChatReturn {
    messages: Message[];
    isLoading: boolean;
    error: string | null;
    sendMessage: (message: string) => Promise<void>;
    clearChat: () => void;
    currentChatId: string | null;
    loadChat: (chatId: string) => void;
    createNewChat: () => void;
}

// API Response Types
export interface ApiChatMessage {
    role: 'user' | 'assistant';
    content: string;
    timestamp: string;
}

export interface ApiChatSession {
    chat_id: string;
    user_id: string;
    title: string;
    created_at: string;
    updated_at: string;
    message_count: number;
}

export interface ApiChatDetail {
    chat_id: string;
    user_id: string;
    title: string;
    created_at: string;
    updated_at: string;
    messages: ApiChatMessage[];
    metadata?: Record<string, any>;
}

export interface GetChatsResponse {
    chats: ApiChatSession[];
    count: number;
}

export interface GetChatResponse {
    chat: ApiChatDetail;
}

export interface CreateChatResponse {
    message: string;
    chat_id: string;
    title: string;
    created_at: string;
    user_id: string;
}

export interface AppendMessageResponse {
    message: string;
    chat_id: string;
    updated_at: string;
    total_messages: number;
}

export interface DeleteChatResponse {
    message: string;
    chat_id: string;
}

// UI Types (converted from API types)
export interface ChatSession {
    id: string;
    title: string;
    lastMessage: string;
    timestamp: Date;
    messageCount: number;
    updatedAt: Date;
}

export interface QueryRequest {
    question: string;
}

export interface RAGResponse {
    answer: string;
    sources: string[];
}

// Enhanced Message type to include sources
export interface Message {
    id: number;
    text: string;
    sender: 'user' | 'bot';
    timestamp: Date;
    role: 'user' | 'assistant' | 'system';
    content: string;
    sources?: string[]; // Add sources field for bot messages
}
