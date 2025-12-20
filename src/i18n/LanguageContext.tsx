/**
 * Language Context Provider
 * Manages language state and provides translation functionality
 * Syncs with Docusaurus i18n system for consistent language switching
 */
import React, { createContext, useContext, useState, useEffect, ReactNode, useMemo } from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import { useLocation } from '@docusaurus/router';

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
  const [isHydrated, setIsHydrated] = useState(false);

  // Get Docusaurus context to sync with i18n locale
  let docusaurusLocale: Language = 'en';
  try {
    const docContext = useDocusaurusContext();
    docusaurusLocale = (docContext?.i18n?.currentLocale || 'en') as Language;
  } catch (e) {
    // Context not available on home page, that's ok
  }

  // Try to get current locale from URL (for docs pages)
  let urlLocale: Language = 'en';
  try {
    const location = useLocation();
    if (location?.pathname?.startsWith('/ur/')) {
      urlLocale = 'ur';
    }
  } catch (e) {
    // Location not available, that's ok
  }

  // Sync language with Docusaurus locale and URL on mount and when they change
  useEffect(() => {
    if (typeof window !== 'undefined') {
      // First, check URL to determine the language
      const detectedLanguage = urlLocale === 'ur' ? 'ur' : 'en';
      setLanguageState(detectedLanguage);
      setIsHydrated(true);
    }
  }, [urlLocale]);

  // Apply RTL direction to document
  useEffect(() => {
    if (typeof document !== 'undefined' && isHydrated) {
      const dir = language === 'ur' ? 'rtl' : 'ltr';
      document.documentElement.setAttribute('dir', dir);
      document.documentElement.setAttribute('lang', language);
      document.body.classList.remove('rtl', 'ltr');
      document.body.classList.add(language === 'ur' ? 'rtl' : 'ltr');
    }
  }, [language, isHydrated]);

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
