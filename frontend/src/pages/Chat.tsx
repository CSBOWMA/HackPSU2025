// pages/Chat.tsx
import { useEffect, useRef, useState } from 'react';
import { useChat } from '../hooks/useChat';
import Message from '../components/chat/Message';
import ChatInput from '../components/chat/ChatInput';
import ChatSidebar from '../components/chat/ChatSidebar';
import './Chat.css';

function Chat() {
    const { messages, isLoading, error, sendMessage, clearChat, currentChatId, loadChat, createNewChat } = useChat();
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const [sidebarRefreshTrigger, setSidebarRefreshTrigger] = useState(0);

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

                <div className="chat-messages">
                    {messages.length === 0 ? (
                        <div className="empty-state">
                            <p>Start a conversation!</p>
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