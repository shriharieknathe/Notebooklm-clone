import React from 'react';
import { FiMessageCircle, FiUser } from 'react-icons/fi';
import './Message.css';

const Message = ({ message, onCitationClick, onSuggestionClick }) => {
  const { type, content, citations, suggestions } = message;

  const renderContent = (content) => {
    // Split content into paragraphs and render each properly
    const paragraphs = content.split('\n').filter(p => p.trim());
    
    return paragraphs.map((paragraph, index) => {
      // Simple markdown-like rendering for bold text within each paragraph
      const parts = paragraph.split('**').map((part, partIndex) => {
        if (partIndex % 2 === 1) {
          return <strong key={partIndex}>{part}</strong>;
        }
        return part;
      });
      
      return (
        <p key={index} className="ai-paragraph">
          {parts}
        </p>
      );
    });
  };

  if (type === 'system') {
    return (
      <div className="message system-message">
        <div className="message-content">
          <div className="system-header">
            <div className="system-icon">📄</div>
            <span className="system-title">{content}</span>
          </div>
          {suggestions && (
            <div className="suggestions">
              <p className="suggestions-text">You can now ask questions about your document. For example:</p>
              <ul className="suggestions-list">
                {suggestions.map((suggestion, index) => (
                  <li key={index}>
                    <button 
                      className="suggestion-button"
                      onClick={() => onSuggestionClick(suggestion)}
                    >
                      {suggestion}
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    );
  }

  if (type === 'user') {
    return (
      <div className="message user-message">
        <div className="message-content">
          <div className="user-header">
            <div className="user-icon">
              <FiUser size={16} />
            </div>
            <span className="user-query">{content}</span>
          </div>
        </div>
      </div>
    );
  }

  if (type === 'ai') {
    return (
      <div className="message ai-message">
        <div className="message-content">
          {/* AI Message Header */}
          <div className="ai-header">
            <div className="ai-header-content">
              <div className="ai-icon">
                <FiMessageCircle size={16} />
              </div>
              <h3 className="ai-question">AI Response</h3>
            </div>
          </div>
          
          {/* AI Message Body */}
          <div className="ai-body">
            <div className="ai-text">
              {renderContent(content)}
            </div>
          </div>
          
          {/* AI Message Footer */}
          <div className="ai-footer">
            {citations && citations.length > 0 && (
              <div className="citations">
                {citations.map((citation, index) => (
                  <button
                    key={index}
                    className="citation-button"
                    onClick={() => onCitationClick(citation.page)}
                  >
                    Page {citation.page}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    );
  }

  return null;
};

export default Message; 