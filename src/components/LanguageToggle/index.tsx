/**
 * Language Toggle Component
 * Uses Docusaurus i18n for proper language switching
 */
import React from 'react';
import { useLocation } from '@docusaurus/router';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import './styles.css';

export function LanguageToggle() {
  const { i18n: { currentLocale, locales, localeConfigs } } = useDocusaurusContext();
  const location = useLocation();

  const switchLocale = () => {
    const newLocale = currentLocale === 'en' ? 'ur' : 'en';

    // Build the new URL with the new locale
    let newPath = location.pathname;

    // Remove current locale prefix if exists
    if (currentLocale !== 'en') {
      newPath = newPath.replace(`/${currentLocale}`, '') || '/';
    }

    // Add new locale prefix (except for default 'en')
    if (newLocale !== 'en') {
      newPath = `/${newLocale}${newPath}`;
    }

    // Navigate to new locale
    window.location.href = newPath;
  };

  const isUrdu = currentLocale === 'ur';

  return (
    <button
      onClick={switchLocale}
      className="language-toggle"
      title={isUrdu ? 'Switch to English' : 'اردو میں تبدیل کریں'}
      aria-label={isUrdu ? 'Switch to English' : 'Switch to Urdu'}
    >
      <span className="language-toggle-icon">
        {isUrdu ? '🇬🇧' : '🇵🇰'}
      </span>
      <span className="language-toggle-text">
        {isUrdu ? 'EN' : 'اردو'}
      </span>
    </button>
  );
}

export default LanguageToggle;
