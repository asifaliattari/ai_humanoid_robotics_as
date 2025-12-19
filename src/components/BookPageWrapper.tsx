/**
 * BookPageWrapper Component
 *
 * Wraps book content pages with AI-native features:
 * - RAG chatbot (floating widget)
 *
 * Usage in MDX:
 * ```mdx
 * import BookPageWrapper from '@site/src/components/BookPageWrapper';
 *
 * <BookPageWrapper sectionId="modules/ros2/index">
 *
 * # Your content here
 *
 * </BookPageWrapper>
 * ```
 */
import React, { useState, useEffect } from 'react';
import { RAGChatWidget } from './RAGChatWidget';

interface BookPageWrapperProps {
  sectionId: string;
  children: React.ReactNode;
}

export const BookPageWrapper: React.FC<BookPageWrapperProps> = ({
  sectionId,
  children,
}) => {
  const [userId, setUserId] = useState<string | null>(null);

  // Get user ID from localStorage
  useEffect(() => {
    const storedUserId = localStorage.getItem('user_id');
    setUserId(storedUserId);
  }, []);

  return (
    <>
      {/* Content */}
      <div className="book-page-content">
        {children}
      </div>

      {/* Floating RAG Chatbot */}
      <RAGChatWidget userId={userId} />

      <style jsx>{`
        .book-page-content {
          margin-bottom: 48px;
        }
      `}</style>
    </>
  );
};

export default BookPageWrapper;
