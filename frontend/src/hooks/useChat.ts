import { useState, useCallback } from 'react';
import type { Message } from '../types/chat.types';
import * as chatApi from '../services/chatApi';

export const useChat = (chatId?: string) => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const sendMessage = useCallback(async (text: string) => {
        if (!text.trim()) return;

        setIsLoading(true);
        setError(null);

        // Add user message immediately
        const userMessage: Message = {
            id: Date.now(),
            text,
            sender: 'user',
            timestamp: new Date(),
            role: 'user',
            content: text,
        };

        setMessages(prev => [...prev, userMessage]);

        try {
            // If there's a chatId, append to existing chat
            if (chatId) {
                await chatApi.appendMessage(chatId, text, 'user');
            } else {
                // Create new chat if no chatId
                await chatApi.createChat(text);
            }

            // Get AI response from RAG system
            const ragResponse = await chatApi.sendMessage(text);

            // Add bot message with answer and sources
            const botMessage: Message = {
                id: Date.now() + 1,
                text: ragResponse.answer,
                sender: 'bot',
                timestamp: new Date(),
                role: 'assistant',
                content: ragResponse.answer,
                sources: ragResponse.sources,
            };

            setMessages(prev => [...prev, botMessage]);

            // If there's a chatId, save the bot response too
            if (chatId) {
                await chatApi.appendMessage(chatId, ragResponse.answer, 'assistant');
            }
        } catch (err) {
            const errorMessage = err instanceof Error ? err.message : 'Failed to send message';
            setError(errorMessage);

            // Add error message to chat
            const errorMsg: Message = {
                id: Date.now() + 1,
                text: `Error: ${errorMessage}`,
                sender: 'bot',
                timestamp: new Date(),
                role: 'assistant',
                content: errorMessage,
            };
            setMessages(prev => [...prev, errorMsg]);
        } finally {
            setIsLoading(false);
        }
    }, [chatId]);

    const loadChat = useCallback(async (id: string) => {
        setIsLoading(true);
        setError(null);

        try {
            const chat = await chatApi.getChatById(id);
            setMessages(chat.messages);
        } catch (err) {
            const errorMessage = err instanceof Error ? err.message : 'Failed to load chat';
            setError(errorMessage);
        } finally {
            setIsLoading(false);
        }
    }, []);

    return {
        messages,
        isLoading,
        error,
        sendMessage,
        loadChat,
        clearChat,
        currentChatId,   
        createNewChat    
    };
};
