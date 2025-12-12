/**
 * RAGChatWidget Component
 *
 * Floating chatbot widget with two modes:
 * 1. Book-wide Q&A: Search entire book with vector similarity
 * 2. Selection-based Q&A: Ask about highlighted text
 */
import React, { useState, useRef, useEffect } from 'react';
import './RAGChatWidget.css';
import { API_ENDPOINTS } from '@site/src/config/api';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  sources?: string[];
}

interface RAGChatWidgetProps {
  userId?: string;
}

export const RAGChatWidget: React.FC<RAGChatWidgetProps> = ({ userId }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    const query = inputValue;
    setInputValue('');
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(API_ENDPOINTS.bookQA, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query,
          user_id: userId || 'guest',
        }),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.answer,
        timestamp: new Date(),
        sources: data.sources?.map((s: any) => s.section_id) || [],
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      console.error('Chat error:', err);
      setError('Could not connect to AI. Make sure backend is running on port 8000.');

      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I could not connect to the AI backend. Please make sure the server is running.',
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const clearChat = () => {
    setMessages([]);
    setError(null);
  };

  return (
    <>
      {/* Floating action button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="rag-fab"
        title="Ask the AI Assistant"
      >
        {isOpen ? '✕' : '💬'}
      </button>

      {/* Chat widget */}
      {isOpen && (
        <div className="rag-chat-widget">
          {/* Header */}
          <div className="chat-header">
            <div className="header-title">
              <span className="icon">🤖</span>
              <span className="title">AI Assistant</span>
            </div>
            <button onClick={clearChat} className="clear-button" title="Clear chat">
              🗑️
            </button>
          </div>

          {/* Mode indicator */}
          <div className="mode-indicator">
            <div className="mode-badge book-wide">
              📚 Ask anything about the book
            </div>
          </div>

          {/* Error banner */}
          {error && (
            <div className="error-banner">
              ⚠️ {error}
            </div>
          )}

          {/* Messages */}
          <div className="chat-messages">
            {messages.length === 0 ? (
              <div className="welcome-message">
                <div className="welcome-icon">👋</div>
                <div className="welcome-text">
                  Hi! I'm your AI assistant for this textbook.
                </div>
                <div className="welcome-hint">
                  <strong>Try asking:</strong>
                  <ul>
                    <li>"What is ROS 2?"</li>
                    <li>"How do digital twins work?"</li>
                    <li>"Explain Isaac Sim"</li>
                  </ul>
                </div>
              </div>
            ) : (
              messages.map((msg) => (
                <div key={msg.id} className={`message ${msg.role}`}>
                  <div className="message-avatar">
                    {msg.role === 'user' ? '👤' : '🤖'}
                  </div>
                  <div className="message-content">
                    <div className="message-text">{msg.content}</div>
                    {msg.sources && msg.sources.length > 0 && (
                      <div className="message-sources">
                        <strong>Sources:</strong>
                        <ul>
                          {msg.sources.slice(0, 3).map((source, idx) => (
                            <li key={idx}>{source}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                    <div className="message-time">
                      {msg.timestamp.toLocaleTimeString()}
                    </div>
                  </div>
                </div>
              ))
            )}
            {isLoading && (
              <div className="message assistant loading">
                <div className="message-avatar">🤖</div>
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="chat-input">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask a question..."
              rows={2}
              disabled={isLoading}
            />
            <button
              onClick={handleSendMessage}
              disabled={isLoading || !inputValue.trim()}
              className="send-button"
            >
              {isLoading ? '⏳' : '➤'}
            </button>
          </div>
        </div>
      )}
    </>
  );
};

export default RAGChatWidget;
