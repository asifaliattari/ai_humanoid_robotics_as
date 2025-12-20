/**
 * RAGChatWidget Component
 *
 * Floating chatbot widget with two modes:
 * 1. Book-wide Q&A: Search entire book with vector similarity
 * 2. Selection-based Q&A: Ask about highlighted text
 */
import React, { useState, useRef, useEffect, useCallback } from 'react';
import './RAGChatWidget.css';
import { API_ENDPOINTS } from '@site/src/config/api';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  sources?: string[];
  context?: string; // Selected text context
}

interface RAGChatWidgetProps {
  userId?: string;
}

interface SelectionPosition {
  x: number;
  y: number;
  text: string;
}

export const RAGChatWidget: React.FC<RAGChatWidgetProps> = ({ userId }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedText, setSelectedText] = useState<string | null>(null);
  const [selectionPosition, setSelectionPosition] = useState<SelectionPosition | null>(null);
  const [mode, setMode] = useState<'book' | 'selection'>('book');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Handle text selection
  const handleTextSelection = useCallback(() => {
    const selection = window.getSelection();
    const text = selection?.toString().trim();

    if (text && text.length > 10 && text.length < 5000) {
      const range = selection?.getRangeAt(0);
      const rect = range?.getBoundingClientRect();

      if (rect) {
        setSelectionPosition({
          x: rect.left + rect.width / 2,
          y: rect.top - 10,
          text: text,
        });
      }
    } else {
      setSelectionPosition(null);
    }
  }, []);

  // Listen for text selection
  useEffect(() => {
    document.addEventListener('mouseup', handleTextSelection);
    document.addEventListener('keyup', handleTextSelection);

    return () => {
      document.removeEventListener('mouseup', handleTextSelection);
      document.removeEventListener('keyup', handleTextSelection);
    };
  }, [handleTextSelection]);

  // Hide selection tooltip when clicking elsewhere
  useEffect(() => {
    const handleClick = (e: MouseEvent) => {
      const target = e.target as HTMLElement;
      if (!target.closest('.selection-tooltip')) {
        // Small delay to allow button click to register
        setTimeout(() => {
          if (!isOpen || mode !== 'selection') {
            setSelectionPosition(null);
          }
        }, 100);
      }
    };

    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, [isOpen, mode]);

  // Handle asking about selected text
  const handleAskAboutSelection = () => {
    if (selectionPosition) {
      setSelectedText(selectionPosition.text);
      setMode('selection');
      setIsOpen(true);
      setSelectionPosition(null);
    }
  };

  // Send message - handles both book-wide and selection-based Q&A
  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date(),
      context: mode === 'selection' ? selectedText || undefined : undefined,
    };

    setMessages((prev) => [...prev, userMessage]);
    const query = inputValue;
    setInputValue('');
    setIsLoading(true);
    setError(null);

    try {
      let response;
      let data;

      if (mode === 'selection' && selectedText) {
        // Selection-based Q&A
        response = await fetch(API_ENDPOINTS.selectionQA, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            selected_text: selectedText,
            query: query,
            user_id: userId || 'guest',
          }),
        });

        if (!response.ok) {
          throw new Error(`API error: ${response.status}`);
        }

        data = await response.json();

        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: data.answer,
          timestamp: new Date(),
        };

        setMessages((prev) => [...prev, assistantMessage]);
      } else {
        // Book-wide Q&A
        response = await fetch(API_ENDPOINTS.bookQA, {
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

        data = await response.json();

        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: data.answer,
          timestamp: new Date(),
          sources: data.sources?.map((s: any) => s.section_id) || [],
        };

        setMessages((prev) => [...prev, assistantMessage]);
      }
    } catch (err) {
      console.error('Chat error:', err);
      setError('Could not connect to AI. Please try again.');

      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I could not connect to the AI backend. Please try again.',
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
    setSelectedText(null);
    setMode('book');
  };

  const switchToBookMode = () => {
    setMode('book');
    setSelectedText(null);
  };

  return (
    <>
      {/* Selection tooltip - appears when text is highlighted */}
      {selectionPosition && (
        <div
          className="selection-tooltip"
          style={{
            position: 'fixed',
            left: `${selectionPosition.x}px`,
            top: `${selectionPosition.y}px`,
            transform: 'translate(-50%, -100%)',
            zIndex: 10001,
          }}
        >
          <button
            onClick={handleAskAboutSelection}
            className="selection-ask-button"
            title="Ask AI about this text"
          >
            🤖 Ask AI
          </button>
        </div>
      )}

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
            {mode === 'selection' && selectedText ? (
              <div className="mode-badge selection-mode">
                <span>📝 Asking about selection</span>
                <button onClick={switchToBookMode} className="mode-switch">
                  Switch to book mode
                </button>
              </div>
            ) : (
              <div className="mode-badge book-wide">
                📚 Ask anything about the book
              </div>
            )}
          </div>

          {/* Selected text preview */}
          {mode === 'selection' && selectedText && (
            <div className="selected-text-preview">
              <strong>Selected text:</strong>
              <p>"{selectedText.length > 150 ? selectedText.substring(0, 150) + '...' : selectedText}"</p>
            </div>
          )}

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
                  {mode === 'selection' ? (
                    <>
                      <strong>Ask about your selection:</strong>
                      <ul>
                        <li>"Explain this in simpler terms"</li>
                        <li>"Give me an example"</li>
                        <li>"What does this mean?"</li>
                      </ul>
                    </>
                  ) : (
                    <>
                      <strong>Try asking:</strong>
                      <ul>
                        <li>"What is ROS 2?"</li>
                        <li>"How do digital twins work?"</li>
                        <li>"Explain Isaac Sim"</li>
                      </ul>
                      <p className="selection-tip">
                        💡 <strong>Tip:</strong> Highlight any text on the page to ask about it!
                      </p>
                    </>
                  )}
                </div>
              </div>
            ) : (
              messages.map((msg) => (
                <div key={msg.id} className={`message ${msg.role}`}>
                  <div className="message-avatar">
                    {msg.role === 'user' ? '👤' : '🤖'}
                  </div>
                  <div className="message-content">
                    {msg.context && (
                      <div className="message-context">
                        Re: "{msg.context.substring(0, 50)}..."
                      </div>
                    )}
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
              placeholder={mode === 'selection' ? "Ask about the selected text..." : "Ask a question..."}
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
