/**
 * Language Context Provider
 * Manages language state and provides translation functionality
 */
import React, { createContext, useContext, useState, useEffect, ReactNode, useMemo } from 'react';

// Import translations directly
import enData from './en.json';
import urData from './ur.json';

// Types
export type Language = 'en' | 'ur';

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

// Translation data - cast to ensure type safety
const translationsData: Record<Language, Translations> = {
  en: enData as Translations,
  ur: urData as Translations,
};

// Create context with default value
const LanguageContext = createContext<LanguageContextType>({
  language: 'en',
  setLanguage: () => {},
  t: (key) => key,
  dir: 'ltr',
  isRTL: false,
  translations: translationsData.en,
});

// Storage key
const LANGUAGE_STORAGE_KEY = 'preferred-language';

// Get nested translation value
function getNestedValue(obj: any, path: string): string {
  if (!obj || !path) return path;

  const keys = path.split('.');
  let value = obj;

  for (const key of keys) {
    if (value && typeof value === 'object' && key in value) {
      value = value[key];
    } else {
      console.warn(`Translation not found for key: ${path}`);
      return path;
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

  // Load saved language preference on mount (client-side only)
  useEffect(() => {
    if (typeof window !== 'undefined') {
      try {
        const savedLanguage = localStorage.getItem(LANGUAGE_STORAGE_KEY);
        if (savedLanguage === 'en' || savedLanguage === 'ur') {
          setLanguageState(savedLanguage);
        }
      } catch (e) {
        console.warn('Could not access localStorage');
      }
    }
  }, []);

  // Apply RTL direction to document
  useEffect(() => {
    if (typeof document !== 'undefined') {
      const dir = language === 'ur' ? 'rtl' : 'ltr';
      document.documentElement.setAttribute('dir', dir);
      document.documentElement.setAttribute('lang', language);
      document.body.classList.remove('rtl', 'ltr');
      document.body.classList.add(language === 'ur' ? 'rtl' : 'ltr');
    }
  }, [language]);

  // Set language and save to localStorage
  const setLanguage = (lang: Language) => {
    setLanguageState(lang);
    if (typeof window !== 'undefined') {
      try {
        localStorage.setItem(LANGUAGE_STORAGE_KEY, lang);
      } catch (e) {
        console.warn('Could not save to localStorage');
      }
    }
  };

  // Memoize context value to prevent unnecessary re-renders
  const value = useMemo<LanguageContextType>(() => {
    const currentTranslations = translationsData[language];

    // Translation function
    const t = (key: string): string => {
      return getNestedValue(currentTranslations, key);
    };

    return {
      language,
      setLanguage,
      t,
      dir: language === 'ur' ? 'rtl' : 'ltr',
      isRTL: language === 'ur',
      translations: currentTranslations,
    };
  }, [language]);

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  );
}

// Hook to use language context
export function useLanguage(): LanguageContextType {
  const context = useContext(LanguageContext);
  return context;
}

// Convenience hook for translations
export function useTranslation() {
  const { t, language, dir, isRTL, setLanguage } = useLanguage();
  return { t, language, dir, isRTL, setLanguage };
}

export default LanguageContext;
