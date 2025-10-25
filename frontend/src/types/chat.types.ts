// types/chat.types.ts
export interface Message {
    id: number;
    text: string;
    sender: 'user' | 'bot';
    timestamp: Date;
}

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

// New types for chat sessions
export interface ChatSession {
    id: string;
    title: string;
    lastMessage: string;
    timestamp: Date;
    messageCount: number;
}

export interface ChatSessionsResponse {
    sessions: ChatSession[];
}

export interface SaveChatRequest {
    chatId: string;
    messages: Message[];
    title?: string;
}