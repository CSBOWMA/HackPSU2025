import type { Message as MessageType } from '../../types/chat.types';
import './Message.css';

interface MessageProps {
    message: MessageType;
}

const Message = ({ message }: MessageProps) => {
    const isBot = message.sender === 'bot';

    return (
        <div className={`message ${isBot ? 'bot' : 'user'}`}>
            <div className="message-content">
                <div className="message-text">
                    {/* Render message with code blocks if present */}
                    {message.text.split('```').map((part, index) => {
                        if (index % 2 === 1) {
                            // This is a code block
                            return (
                                <pre key={index} className="code-block">
                                    <code>{part}</code>
                                </pre>
                            );
                        }
                        // Regular text
                        return <span key={index}>{part}</span>;
                    })}
                </div>
                {message.sources && message.sources.length > 0 && (
                    <div className="message-sources">
                        <strong>Sources:</strong>
                        <ul>
                            {message.sources.map((source, idx) => (
                                <li key={idx}>{source}</li>
                            ))}
                        </ul>
                    </div>
                )}
                <span className="message-timestamp">
                    {message.timestamp.toLocaleTimeString()}
                </span>
            </div>
        </div>
    );
};

export default Message;