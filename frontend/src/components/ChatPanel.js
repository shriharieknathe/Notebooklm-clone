import React, { useState, useRef, useEffect } from 'react';
import { FiX, FiSend } from 'react-icons/fi';
import Message from './Message';
import './ChatPanel.css';

const ChatPanel = ({ messages, onSendMessage, onCitationClick, onRemoveDocument, isLoading }) => {
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (inputValue.trim() && !isLoading) {
      const message = inputValue.trim();
      setInputValue('');
      
      await onSendMessage(message);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setInputValue(suggestion);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      handleSubmit(e);
    }
  };

  return (
    <div className="chat-panel">
      <div className="chat-header">
        <div className="chat-header-content">
          <div className="document-icon">📄</div>
          <span className="header-text">Your document is ready!</span>
        </div>
        <button className="close-button" onClick={onRemoveDocument}>
          <FiX size={16} />
        </button>
      </div>

      <div className="chat-messages">
        {messages.map((message) => (
          <Message 
            key={message.id}
            message={message}
            onCitationClick={onCitationClick}
            onSuggestionClick={handleSuggestionClick}
          />
        ))}
        {isLoading && (
          <div className="typing-indicator">
            <div className="typing-dots">
              <div className="dot"></div>
              <div className="dot"></div>
              <div className="dot"></div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form className="chat-input-container" onSubmit={handleSubmit}>
        <input
          type="text"
          className="chat-input"
          placeholder="Ask about the document..."
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={isLoading}
        />
        <button 
          type="submit" 
          className="send-button"
          disabled={!inputValue.trim() || isLoading}
        >
          <FiSend size={16} />
        </button>
      </form>
    </div>
  );
};

export default ChatPanel; 