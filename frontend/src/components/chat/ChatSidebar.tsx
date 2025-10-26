// components/chat/ChatSidebar.tsx
import { useEffect, useState, useCallback } from 'react';
import type { ChatSession } from '../../types/chat.types';
import { getChatSessions, deleteChat } from '../../services/chatApi';
import './ChatSidebar.css';

interface ChatSidebarProps {
    currentChatId: string | null;
    onSelectChat: (chatId: string) => void;
    onNewChat: () => void;
    refreshTrigger?: number; // Add this to trigger refresh from parent
}

function ChatSidebar({ currentChatId, onSelectChat, onNewChat, refreshTrigger }: ChatSidebarProps) {
    const [sessions, setSessions] = useState<ChatSession[]>([]);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    const loadSessions = useCallback(async () => {
        setIsLoading(true);
        setError(null);
        try {
            const chatSessions = await getChatSessions();
            setSessions(chatSessions);
        } catch (err) {
            setError('Failed to load chat history');
            console.error('Error loading sessions:', err);
        } finally {
            setIsLoading(false);
        }
    }, []);

    // Load sessions on mount and when refreshTrigger changes
    useEffect(() => {
        loadSessions();
    }, [loadSessions, refreshTrigger]);

    const handleDeleteChat = async (chatId: string, e: React.MouseEvent) => {
        e.stopPropagation();

        if (!window.confirm('Are you sure you want to delete this chat?')) {
            return;
        }

        try {
            await deleteChat(chatId);
            setSessions(prev => prev.filter(session => session.id !== chatId));

            if (currentChatId === chatId) {
                onNewChat();
            }
        } catch (err) {
            console.error('Error deleting chat:', err);
            alert('Failed to delete chat');
        }
    };

    const formatTimestamp = (date: Date): string => {
        const now = new Date();
        const diffInMs = now.getTime() - new Date(date).getTime();
        const diffInHours = diffInMs / (1000 * 60 * 60);
        const diffInDays = diffInHours / 24;

        if (diffInHours < 1) {
            return 'Just now';
        } else if (diffInHours < 24) {
            return 'Today';
        } else if (diffInDays < 2) {
            return 'Yesterday';
        } else if (diffInDays < 7) {
            return `${Math.floor(diffInDays)} days ago`;
        } else {
            return new Date(date).toLocaleDateString();
        }
    };

    return (
        <div className="chat-sidebar">
            <div className="sidebar-header">
                <h2>Chat History</h2>
                <button onClick={onNewChat} className="new-chat-button" title="New Chat">
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                        <path d="M10 4V16M4 10H16" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                    </svg>
                </button>
            </div>

            <div className="sidebar-content">
                {isLoading && (
                    <div className="sidebar-loading">
                        <div className="loading-spinner"></div>
                        Loading chats...
                    </div>
                )}

                {error && (
                    <div className="sidebar-error">
                        {error}
                        <button onClick={loadSessions} className="retry-button">
                            Retry
                        </button>
                    </div>
                )}

                {!isLoading && sessions.length === 0 && (
                    <div className="sidebar-empty">
                        <p>No chat history yet</p>
                        <p className="sidebar-empty-hint">Start a conversation to see it here</p>
                    </div>
                )}

                {!isLoading && sessions.length > 0 && (
                    <div className="chat-sessions">
                        {sessions.map((session) => (
                            <div
                                key={session.id}
                                className={`chat-session-item ${currentChatId === session.id ? 'active' : ''}`}
                                onClick={() => onSelectChat(session.id)}
                            >
                                <div className="session-content">
                                    <h3 className="session-title">{session.title}</h3>
                                    <div className="session-meta">
                                        <span className="session-time">
                                            {formatTimestamp(session.updatedAt)}
                                        </span>
                                        <span className="session-count">
                                            {session.messageCount} {session.messageCount === 1 ? 'message' : 'messages'}
                                        </span>
                                    </div>
                                </div>
                                <button
                                    className="delete-chat-button"
                                    onClick={(e) => handleDeleteChat(session.id, e)}
                                    title="Delete chat"
                                >
                                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                                        <path d="M2 4H14M6 4V2H10V4M3 4V14H13V4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                                    </svg>
                                </button>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}

export default ChatSidebar;