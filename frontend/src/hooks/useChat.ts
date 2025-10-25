// hooks/useChat.ts
import { useState, useCallback, useEffect } from 'react';
import { sendMessage as sendMessageApi, saveChat, getChatById } from '../services/chatApi';
import type { Message, UseChatReturn } from '../types/chat.types';

export const useChat = (): UseChatReturn => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);
    const [currentChatId, setCurrentChatId] = useState<string | null>(null);

    // Generate a new chat ID
    const generateChatId = (): string => {
        return `chat_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    };

    // Initialize with a new chat
    useEffect(() => {
        if (!currentChatId) {
            setCurrentChatId(generateChatId());
        }
    }, [currentChatId]);

    // Save chat whenever messages change
    useEffect(() => {
        if (currentChatId && messages.length > 0) {
            saveChat({
                chatId: currentChatId,
                messages,
            }).catch(err => console.error('Error auto-saving chat:', err));
        }
    }, [messages, currentChatId]);

    const sendMessage = useCallback(async (userMessage: string): Promise<void> => {
        if (!userMessage.trim() || !currentChatId) return;

        // Add user message to chat
        const userMessageObj: Message = {
            id: Date.now(),
            text: userMessage,
            sender: 'user',
            timestamp: new Date(),
        };

        setMessages(prev => [...prev, userMessageObj]);
        setIsLoading(true);
        setError(null);

        try {
            // Call API
            const botResponse = await sendMessageApi(userMessage);

            // Add bot response to chat
            const botMessageObj: Message = {
                id: Date.now() + 1,
                text: botResponse,
                sender: 'bot',
                timestamp: new Date(),
            };

            setMessages(prev => [...prev, botMessageObj]);
        } catch (err) {
            setError('Failed to send message. Please try again.');
            console.error('Chat error:', err);
        } finally {
            setIsLoading(false);
        }
    }, [currentChatId]);

    const clearChat = useCallback((): void => {
        setMessages([]);
        setError(null);
    }, []);

    const loadChat = useCallback(async (chatId: string): Promise<void> => {
        setIsLoading(true);
        setError(null);

        try {
            const chatData = await getChatById(chatId);
            setMessages(chatData.messages || []);
            setCurrentChatId(chatId);
        } catch (err) {
            setError('Failed to load chat');
            console.error('Error loading chat:', err);
        } finally {
            setIsLoading(false);
        }
    }, []);

    const createNewChat = useCallback((): void => {
        setMessages([]);
        setError(null);
        setCurrentChatId(generateChatId());
    }, []);

    return {
        messages,
        isLoading,
        error,
        sendMessage,
        clearChat,
        currentChatId,
        loadChat,
        createNewChat,
    };
};