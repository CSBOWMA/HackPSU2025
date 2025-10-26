// pages/Chat.tsx
import { useEffect, useRef, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { useChat } from '../hooks/useChat';
import Message from '../components/chat/Message';
import ChatInput from '../components/chat/ChatInput';
import ChatSidebar from '../components/chat/ChatSidebar';
import './Chat.css';

function Chat() {
    const location = useLocation();
    const { messages, isLoading, error, sendMessage, clearChat, currentChatId, loadChat, createNewChat } = useChat();
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const [sidebarRefreshTrigger, setSidebarRefreshTrigger] = useState(0);

    // Get class context from navigation state
    const classContext = location.state as { classId?: string; className?: string } | null;

    const scrollToBottom = (): void => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    // Trigger sidebar refresh when messages change (new chat or message sent)
    useEffect(() => {
        if (messages.length > 0) {
            setSidebarRefreshTrigger(prev => prev + 1);
        }
    }, [messages.length, currentChatId]);

    // Optional: Auto-create new chat when coming from a class
    useEffect(() => {
        if (classContext?.className && messages.length === 0) {
            console.log('Chat opened for class:', classContext.className);
            // You could create a new chat automatically here if desired
            // createNewChat();
        }
    }, [classContext, messages.length]);

    const handleSendMessage = async (message: string) => {
        await sendMessage(message);
        // Sidebar will refresh automatically due to useEffect above
    };

    return (
        <div className="chat-page">
            <ChatSidebar
                currentChatId={currentChatId}
                onSelectChat={loadChat}
                onNewChat={createNewChat}
                refreshTrigger={sidebarRefreshTrigger}
            />

            <div className="chat-container">
                <div className="chat-header">
                    <h2>Chat</h2>
                    {messages.length > 0 && (
                        <button onClick={clearChat} className="clear-button">
                            Clear Chat
                        </button>
                    )}
                </div>

                {/* Class Context Banner */}
                {classContext?.className && (
                    <div className="chat-context-banner">
                        <span className="context-icon">📚</span>
                        <div className="context-text">
                            <span className="context-label">Chatting about:</span>
                            <strong>{classContext.className}</strong>
                        </div>
                    </div>
                )}

                <div className="chat-messages">
                    {messages.length === 0 ? (
                        <div className="empty-state">
                            {classContext?.className ? (
                                <>
                                    <div className="empty-icon">💬</div>
                                    <h3>Ask about {classContext.className}</h3>
                                    <p>I can help you with course materials, assignments, and concepts.</p>
                                    <div className="suggestion-chips">
                                        <button
                                            className="suggestion-chip"
                                            onClick={() => handleSendMessage(`What topics are covered in ${classContext.className}?`)}
                                        >
                                            What topics are covered?
                                        </button>
                                        <button
                                            className="suggestion-chip"
                                            onClick={() => handleSendMessage(`What assignments are due soon?`)}
                                        >
                                            Upcoming assignments?
                                        </button>
                                        <button
                                            className="suggestion-chip"
                                            onClick={() => handleSendMessage(`Explain the latest lecture`)}
                                        >
                                            Explain latest lecture
                                        </button>
                                    </div>
                                </>
                            ) : (
                                <>
                                    <div className="empty-icon">👋</div>
                                    <h3>Start a conversation!</h3>
                                    <p>Ask me anything about your classes.</p>
                                </>
                            )}
                        </div>
                    ) : (
                        messages.map((message) => (
                            <Message key={message.id} message={message} />
                        ))
                    )}
                    {error && (
                        <div className="error-message">
                            {error}
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>

                <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
            </div>
        </div>
    );
}

export default Chat;