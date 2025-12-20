/**
 * i18n - Internationalization module
 * Provides language switching between English and Urdu with RTL support
 */

export {
  LanguageProvider,
  useLanguage,
  useTranslation,
  default as LanguageContext,
} from './LanguageContext';

export type { Language } from './LanguageContext';

// Re-export translation files for direct access if needed
export { default as enTranslations } from './en.json';
export { default as urTranslations } from './ur.json';
