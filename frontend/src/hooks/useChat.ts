// hooks/useChat.ts
import { useState, useCallback, useEffect } from 'react';
import {
    getChatById,
    createChat,
    appendMessage,
    sendMessage as sendMessageApi
} from '../services/chatApi';
import type { Message, UseChatReturn } from '../types/chat.types';

export const useChat = (): UseChatReturn => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);
    const [currentChatId, setCurrentChatId] = useState<string | null>(null);

    const sendMessage = useCallback(async (userMessage: string): Promise<void> => {
        if (!userMessage.trim()) return;

        // Add user message to UI immediately for better UX
        const userMessageObj: Message = {
            id: Date.now(),
            text: userMessage,
            sender: 'user',
            timestamp: new Date(),
            role: 'user',
            content: userMessage,
        };

        setMessages(prev => [...prev, userMessageObj]);
        setIsLoading(true);
        setError(null);

        try {
            let chatId = currentChatId;

            // If no chat exists, create a new one
            if (!chatId) {
                const createResponse = await createChat(userMessage);
                chatId = createResponse.chat_id;
                setCurrentChatId(chatId);
            } else {
                // Append message to existing chat
                await appendMessage(chatId, userMessage, 'user');
            }

            // Get AI response (you'll need to implement this based on your API)
            const botResponse = await sendMessageApi(userMessage);

            // Append AI response to the chat
            if (chatId) {
                await appendMessage(chatId, botResponse, 'assistant');
            }

            // Add bot response to UI
            const botMessageObj: Message = {
                id: Date.now() + 1,
                text: botResponse,
                sender: 'bot',
                timestamp: new Date(),
                role: 'assistant',
                content: botResponse,
            };

            setMessages(prev => [...prev, botMessageObj]);
        } catch (err) {
            setError('Failed to send message. Please try again.');
            console.error('Chat error:', err);

            // Remove the user message from UI if sending failed
            setMessages(prev => prev.filter(msg => msg.id !== userMessageObj.id));
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
        setCurrentChatId(null); // Set to null, will be created on first message
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