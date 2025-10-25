import { useEffect, useRef } from 'react';
import { useChat } from '../hooks/useChat';
import Message from '../components/chat/Message';
import ChatInput from '../components/chat/ChatInput';
import './Chat.css';

function Chat() {
    const { messages, isLoading, error, sendMessage, clearChat } = useChat();
    const messagesEndRef = useRef<HTMLDivElement>(null);

    // Auto-scroll to bottom when new messages arrive
    const scrollToBottom = (): void => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    return (
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

            <ChatInput onSendMessage={sendMessage} isLoading={isLoading} />
        </div>
    );
}

export default Chat;