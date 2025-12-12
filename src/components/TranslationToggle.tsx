/**
 * TranslationToggle Component
 *
 * 5-language selector for translating book content
 * Supports: English, Urdu, French, Arabic, German
 * Handles RTL layout for Urdu and Arabic
 */
import React, { useState } from 'react';
import { API_ENDPOINTS } from '../config/api';
import './TranslationToggle.css';

interface Language {
  code: string;
  name: string;
  direction: 'ltr' | 'rtl';
  flag: string; // Emoji flag
}

const LANGUAGES: Language[] = [
  { code: 'en', name: 'English', direction: 'ltr', flag: '🇬🇧' },
  { code: 'ur', name: 'اردو', direction: 'rtl', flag: '🇵🇰' },
  { code: 'fr', name: 'Français', direction: 'ltr', flag: '🇫🇷' },
  { code: 'ar', name: 'العربية', direction: 'rtl', flag: '🇸🇦' },
  { code: 'de', name: 'Deutsch', direction: 'ltr', flag: '🇩🇪' },
];

interface TranslationToggleProps {
  sectionId: string;
  onTranslate: (targetLanguage: string, translatedContent: string) => void;
  onReset: () => void;
}

export const TranslationToggle: React.FC<TranslationToggleProps> = ({
  sectionId,
  onTranslate,
  onReset,
}) => {
  const [selectedLanguage, setSelectedLanguage] = useState<string>('en');
  const [isTranslating, setIsTranslating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleLanguageChange = async (languageCode: string) => {
    // If selecting English, just reset to original
    if (languageCode === 'en') {
      setSelectedLanguage('en');
      onReset();
      return;
    }

    // If already selected, do nothing
    if (languageCode === selectedLanguage) {
      return;
    }

    setIsTranslating(true);
    setError(null);

    try {
      // Call translation API
      const response = await fetch(API_ENDPOINTS.translate, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          section_id: sectionId,
          target_language: languageCode,
        }),
      });

      if (!response.ok) {
        throw new Error('Translation failed');
      }

      const data = await response.json();

      // Update UI with translated content
      setSelectedLanguage(languageCode);
      onTranslate(languageCode, data.translated_content);

      // Log cache hit status
      console.log(
        `Translation ${data.cache_hit ? 'cached' : 'generated'} in ${data.translation_time_ms}ms`
      );
    } catch (err) {
      setError('Translation failed. Please try again.');
      console.error('Translation error:', err);
    } finally {
      setIsTranslating(false);
    }
  };

  return (
    <div className="translation-toggle">
      <div className="translation-label">
        🌐 Language:
      </div>

      <div className="translation-buttons">
        {LANGUAGES.map((lang) => (
          <button
            key={lang.code}
            onClick={() => handleLanguageChange(lang.code)}
            disabled={isTranslating}
            className={`translation-button ${
              selectedLanguage === lang.code ? 'active' : ''
            } ${isTranslating ? 'disabled' : ''}`}
            title={lang.name}
          >
            <span className="flag">{lang.flag}</span>
            <span className="lang-name">{lang.name}</span>
          </button>
        ))}
      </div>

      {isTranslating && (
        <div className="translation-loading">
          <span className="spinner">⏳</span> Translating...
        </div>
      )}

      {error && (
        <div className="translation-error">
          ⚠️ {error}
        </div>
      )}
    </div>
  );
};

export default TranslationToggle;
