/**
 * BookPageWrapper Component
 *
 * Wraps book content pages with AI-native features:
 * - Translation toggle (5 languages)
 * - Personalization button
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
import { TranslationToggle } from './TranslationToggle';
import { PersonalizeButton } from './PersonalizeButton';
import { RAGChatWidget } from './RAGChatWidget';

interface BookPageWrapperProps {
  sectionId: string;
  children: React.ReactNode;
}

export const BookPageWrapper: React.FC<BookPageWrapperProps> = ({
  sectionId,
  children,
}) => {
  const [originalContent, setOriginalContent] = useState<string>('');
  const [displayContent, setDisplayContent] = useState<React.ReactNode>(children);
  const [userId, setUserId] = useState<string | null>(null);
  const [contentLanguage, setContentLanguage] = useState<string>('en');
  const [isPersonalized, setIsPersonalized] = useState(false);

  // Get user ID from localStorage (set by Better-Auth)
  useEffect(() => {
    const storedUserId = localStorage.getItem('user_id');
    setUserId(storedUserId);
  }, []);

  // Store original content on mount
  useEffect(() => {
    setOriginalContent(children as string);
  }, [children]);

  const handleTranslate = (targetLanguage: string, translatedContent: string) => {
    setContentLanguage(targetLanguage);

    // Apply RTL if needed
    const direction = ['ur', 'ar'].includes(targetLanguage) ? 'rtl' : 'ltr';

    setDisplayContent(
      <div dir={direction} dangerouslySetInnerHTML={{ __html: translatedContent }} />
    );
  };

  const handleResetTranslation = () => {
    setContentLanguage('en');
    setDisplayContent(children);
  };

  const handlePersonalize = (adaptedContent: string, adaptations: any[]) => {
    setIsPersonalized(true);
    setDisplayContent(
      <div dangerouslySetInnerHTML={{ __html: adaptedContent }} />
    );
  };

  const handleResetPersonalization = () => {
    setIsPersonalized(false);
    setDisplayContent(children);
  };

  return (
    <>
      {/* Control Panel */}
      <div className="book-page-controls">
        <TranslationToggle
          sectionId={sectionId}
          onTranslate={handleTranslate}
          onReset={handleResetTranslation}
        />

        <PersonalizeButton
          sectionId={sectionId}
          userId={userId}
          onPersonalize={handlePersonalize}
          onReset={handleResetPersonalization}
        />
      </div>

      {/* Content */}
      <div className="book-page-content">
        {displayContent}
      </div>

      {/* Floating RAG Chatbot */}
      <RAGChatWidget userId={userId} />

      <style jsx>{`
        .book-page-controls {
          display: flex;
          flex-direction: column;
          gap: 16px;
          margin-bottom: 32px;
          padding: 20px;
          background: var(--ifm-background-surface-color);
          border-radius: 12px;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }

        .book-page-content {
          margin-bottom: 48px;
        }

        /* Mobile responsive */
        @media (max-width: 768px) {
          .book-page-controls {
            padding: 16px;
          }
        }
      `}</style>
    </>
  );
};

export default BookPageWrapper;
