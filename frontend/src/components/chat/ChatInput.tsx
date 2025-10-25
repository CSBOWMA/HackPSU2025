import React, { useState } from 'react';
import './ChatInput.css';

interface ChatInputProps {
    onSendMessage: (message: string) => void;
    isLoading: boolean;
}

function ChatInput({ onSendMessage, isLoading }: ChatInputProps) {
    const [inputValue, setInputValue] = useState<string>('');

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>): void => {
        e.preventDefault();
        if (inputValue.trim() && !isLoading) {
            onSendMessage(inputValue);
            setInputValue('');
        }
    };

    const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>): void => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            const form = e.currentTarget.form;
            if (form) {
                handleSubmit(new Event('submit') as any);
            }
        }
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>): void => {
        setInputValue(e.target.value);
    };

    return (
        <form className="chat-input-form" onSubmit={handleSubmit}>
            <input
                type="text"
                value={inputValue}
                onChange={handleChange}
                onKeyPress={handleKeyPress}
                placeholder={isLoading ? "Waiting for response..." : "Type your message..."}
                disabled={isLoading}
                className="chat-input"
            />
            <button
                type="submit"
                disabled={isLoading || !inputValue.trim()}
                className="send-button"
            >
                {isLoading ? '...' : 'Send'}
            </button>
        </form>
    );
}

export default ChatInput;