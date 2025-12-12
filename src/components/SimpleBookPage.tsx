/**
 * SimpleBookPage - English Only Version
 * Just RAG Chatbot, no translation or personalization
 */
import React from 'react';
import { RAGChatWidget } from './RAGChatWidget';

interface SimpleBookPageProps {
  children: React.ReactNode;
}

export const SimpleBookPage: React.FC<SimpleBookPageProps> = ({ children }) => {
  return (
    <>
      {/* Content */}
      <div className="book-content">
        {children}
      </div>

      {/* RAG Chatbot Only */}
      <RAGChatWidget userId={null} />
    </>
  );
};

export default SimpleBookPage;
