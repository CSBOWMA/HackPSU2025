import type { Message as MessageType } from '../../types/chat.types';
import './Message.css';

interface MessageProps {
    message: MessageType;
}

function Message({ message }: MessageProps) {
    const isUser = message.sender === 'user';

    return (
        <div className={`message-wrapper ${isUser ? 'user' : 'bot'}`}>
            <div className={`message ${isUser ? 'user-message' : 'bot-message'}`}>
                <p>{message.text}</p>
                <span className="timestamp">
                    {new Date(message.timestamp).toLocaleTimeString([], {
                        hour: '2-digit',
                        minute: '2-digit'
                    })}
                </span>
            </div>
        </div>
    );
}

export default Message;