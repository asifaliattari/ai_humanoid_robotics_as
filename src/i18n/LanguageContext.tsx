/**
 * Language Context Provider
 * Manages language state and provides translation functionality
 */
import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import enTranslations from './en.json';
import urTranslations from './ur.json';

// Types
export type Language = 'en' | 'ur';
export type TranslationKey = string;

interface Translations {
  [key: string]: any;
}

interface LanguageContextType {
  language: Language;
  setLanguage: (lang: Language) => void;
  t: (key: string) => string;
  dir: 'ltr' | 'rtl';
  isRTL: boolean;
  translations: Translations;
}

// Translation data
const translations: Record<Language, Translations> = {
  en: enTranslations,
  ur: urTranslations,
};

// Create context
const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

// Storage key
const LANGUAGE_STORAGE_KEY = 'preferred-language';

// Get nested translation value
function getNestedValue(obj: any, path: string): string {
  const keys = path.split('.');
  let value = obj;

  for (const key of keys) {
    if (value && typeof value === 'object' && key in value) {
      value = value[key];
    } else {
      return path; // Return key if translation not found
    }
  }

  return typeof value === 'string' ? value : path;
}

// Provider component
interface LanguageProviderProps {
  children: ReactNode;
}

export function LanguageProvider({ children }: LanguageProviderProps) {
  const [language, setLanguageState] = useState<Language>('en');
  const [isInitialized, setIsInitialized] = useState(false);

  // Load saved language preference on mount
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const savedLanguage = localStorage.getItem(LANGUAGE_STORAGE_KEY) as Language;
      if (savedLanguage && (savedLanguage === 'en' || savedLanguage === 'ur')) {
        setLanguageState(savedLanguage);
      }
      setIsInitialized(true);
    }
  }, []);

  // Apply RTL direction to document
  useEffect(() => {
    if (typeof document !== 'undefined' && isInitialized) {
      const dir = language === 'ur' ? 'rtl' : 'ltr';
      document.documentElement.setAttribute('dir', dir);
      document.documentElement.setAttribute('lang', language);
      document.body.classList.toggle('rtl', language === 'ur');
      document.body.classList.toggle('ltr', language === 'en');
    }
  }, [language, isInitialized]);

  // Set language and save to localStorage
  const setLanguage = (lang: Language) => {
    setLanguageState(lang);
    if (typeof window !== 'undefined') {
      localStorage.setItem(LANGUAGE_STORAGE_KEY, lang);
    }
  };

  // Translation function
  const t = (key: string): string => {
    return getNestedValue(translations[language], key);
  };

  // Direction helpers
  const dir = language === 'ur' ? 'rtl' : 'ltr';
  const isRTL = language === 'ur';

  const value: LanguageContextType = {
    language,
    setLanguage,
    t,
    dir,
    isRTL,
    translations: translations[language],
  };

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  );
}

// Hook to use language context
export function useLanguage(): LanguageContextType {
  const context = useContext(LanguageContext);
  if (context === undefined) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
}

// Convenience hook for translations
export function useTranslation() {
  const { t, language, dir, isRTL } = useLanguage();
  return { t, language, dir, isRTL };
}

export default LanguageContext;
