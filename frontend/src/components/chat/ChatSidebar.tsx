// components/chat/ChatSidebar.tsx
import { useEffect, useState } from 'react';
import { ChatSession } from '../../types/chat.types';
import { getChatSessions, deleteChat } from '../../services/chatApi';
import './ChatSidebar.css';

interface ChatSidebarProps {
    currentChatId: string | null;
    onSelectChat: (chatId: string) => void;
    onNewChat: () => void;
}

function ChatSidebar({ currentChatId, onSelectChat, onNewChat }: ChatSidebarProps) {
    const [sessions, setSessions] = useState<ChatSession[]>([]);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    const loadSessions = async () => {
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
    };

    useEffect(() => {
        loadSessions();
    }, []);

    const handleDeleteChat = async (chatId: string, e: React.MouseEvent) => {
        e.stopPropagation(); // Prevent triggering onSelectChat

        if (!window.confirm('Are you sure you want to delete this chat?')) {
            return;
        }

        try {
            await deleteChat(chatId);
            setSessions(prev => prev.filter(session => session.id !== chatId));

            // If deleted chat was the current one, create a new chat
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

        if (diffInHours < 24) {
            return 'Today';
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
                    <div className="sidebar-loading">Loading chats...</div>
                )}

                {error && (
                    <div className="sidebar-error">{error}</div>
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
                                    <p className="session-preview">{session.lastMessage}</p>
                                    <div className="session-meta">
                                        <span className="session-time">
                                            {formatTimestamp(session.timestamp)}
                                        </span>
                                        <span className="session-count">
                                            {session.messageCount} messages
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