/**
 * Root component - wraps the entire Docusaurus site
 * This adds the RAG chatbot to ALL pages
 */
import React from 'react';
import { RAGChatWidget } from '../components/RAGChatWidget';

export default function Root({children}) {
  return (
    <>
      {children}
      {/* Add chatbot to all pages */}
      <RAGChatWidget userId={null} />
    </>
  );
}
