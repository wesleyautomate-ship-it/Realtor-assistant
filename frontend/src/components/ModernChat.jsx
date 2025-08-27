import React, { useState, useRef, useEffect } from 'react';

const ModernChat = ({ 
  messages, 
  onSendMessage, 
  isLoading, 
  selectedRole, 
  onRoleChange,
  onClearChat,
  isSaving,
  sessionId
}) => {
  const [inputMessage, setInputMessage] = useState('');
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputMessage.trim() && !isLoading) {
      onSendMessage(inputMessage);
      setInputMessage('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    });
  };

  const getRoleIcon = (role) => {
    const icons = {
      client: '👤',
      agent: '🏠',
      employee: '👨‍💼',
      admin: '⚙️'
    };
    return icons[role] || '👤';
  };

  return (
    <div className="chat-container">
      {/* Page Header */}
      <div className="page-header">
        <div className="flex items-center justify-between">
          <div>
            <div className="page-title">AI Assistant</div>
            <div className="page-subtitle">Role: {selectedRole}</div>
          </div>
          <div className="flex items-center gap-3">
            {messages.length > 0 && (
              <button
                onClick={onClearChat}
                className="px-3 py-2 text-sm bg-surface hover:bg-surface-hover border border-border-primary rounded-lg transition-colors"
                title="Clear chat"
                style={{
                  padding: 'var(--space-3) var(--space-4)',
                  fontSize: 'var(--font-size-sm)',
                  background: 'var(--bg-surface)',
                  border: '1px solid var(--border-primary)',
                  borderRadius: 'var(--radius-lg)',
                  transition: 'all var(--transition-fast)',
                  color: 'var(--text-primary)'
                }}
                onMouseOver={(e) => {
                  e.target.style.background = 'var(--bg-surface-hover)';
                }}
                onMouseOut={(e) => {
                  e.target.style.background = 'var(--bg-surface)';
                }}
              >
                🗑️ Clear
              </button>
            )}
            {isSaving && (
              <div className="flex items-center gap-2 text-sm text-text-tertiary">
                <div className="loading-spinner"></div>
                <span>Saving...</span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Messages Container */}
      <div className="messages-container">
        {messages.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">💬</div>
            <h3 className="empty-title">Start a conversation</h3>
            <p className="empty-description">
              Ask me about Dubai real estate properties, market trends, or any property-related questions.
            </p>
            <div className="suggestions">
              <div className="suggestion-title">Try asking:</div>
              <div className="suggestion-chips">
                <button 
                  className="suggestion-chip"
                  onClick={() => onSendMessage("Show me properties in Dubai Marina")}
                >
                  Show me properties in Dubai Marina
                </button>
                <button 
                  className="suggestion-chip"
                  onClick={() => onSendMessage("What are the current market trends in Dubai?")}
                >
                  What are the current market trends in Dubai?
                </button>
                <button 
                  className="suggestion-chip"
                  onClick={() => onSendMessage("I'm looking for a 2-bedroom apartment under 2M AED")}
                >
                  I'm looking for a 2-bedroom apartment under 2M AED
                </button>
              </div>
            </div>
          </div>
        ) : (
          messages.map((message, index) => (
            <div 
              key={message.id || index} 
              className={`message ${message.sender === 'user' ? 'user' : 'ai'}`}
            >
              <div className="message-avatar">
                {message.sender === 'user' ? getRoleIcon(selectedRole) : '🤖'}
              </div>
              <div className="message-content">
                <div className="message-bubble">
                  {message.text}
                </div>
                <div className="message-meta">
                  <span className="message-time">
                    {formatTime(message.timestamp)}
                  </span>
                  {message.sender === 'user' && (
                    <span className="message-role">
                      {selectedRole}
                    </span>
                  )}
                </div>
              </div>
            </div>
          ))
        )}
        
        {isLoading && (
          <div className="message ai">
            <div className="message-avatar">🤖</div>
            <div className="message-content">
              <div className="message-bubble loading">
                <div className="loading-dots">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Chat Input */}
      <div className="chat-input-container">
        <form onSubmit={handleSubmit} className="chat-input-form">
          <div className="chat-input-wrapper">
            <textarea
              ref={inputRef}
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask about properties, market trends, or any real estate questions..."
              className="chat-input"
              rows={1}
              disabled={isLoading}
            />
          </div>
          <button
            type="submit"
            disabled={!inputMessage.trim() || isLoading}
            className="send-button"
          >
            {isLoading ? (
              <div className="loading-spinner"></div>
            ) : (
              <>
                <span>🚀</span>
                <span className="hidden sm:inline">Send</span>
              </>
            )}
          </button>
        </form>
      </div>
    </div>
  );
};

export default ModernChat;

