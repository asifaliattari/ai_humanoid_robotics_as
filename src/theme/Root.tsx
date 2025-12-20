/**
 * Root component - wraps the entire Docusaurus site
 * This adds the Language Provider and RAG chatbot to ALL pages
 */
import React from 'react';
import { LanguageProvider } from '../i18n';
import { RAGChatWidget } from '../components/RAGChatWidget';

interface RootProps {
  children: React.ReactNode;
}

export default function Root({ children }: RootProps) {
  return (
    <LanguageProvider>
      {children}
      {/* Add chatbot to all pages */}
      <RAGChatWidget userId={null} />
    </LanguageProvider>
  );
}
