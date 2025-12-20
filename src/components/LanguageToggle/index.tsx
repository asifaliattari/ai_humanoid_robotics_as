/**
 * Language Toggle Component
 * Syncs with Docusaurus i18n and React Context for consistent language switching
 */
import React, { useEffect, useState } from 'react';
import { useLocation } from '@docusaurus/router';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import { useTranslation } from '@site/src/i18n';
import './styles.css';

export function LanguageToggle() {
  const [isUrdu, setIsUrdu] = useState(false);
  const { i18n: { currentLocale } } = useDocusaurusContext();
  const location = useLocation();
  const { setLanguage } = useTranslation();

  // Sync button state with current locale
  useEffect(() => {
    setIsUrdu(currentLocale === 'ur');
    setLanguage(currentLocale === 'ur' ? 'ur' : 'en');
  }, [currentLocale, setLanguage]);

  const switchLocale = () => {
    const newLocale = currentLocale === 'en' ? 'ur' : 'en';

    // Update React Context to match Docusaurus locale
    setLanguage(newLocale);

    // Build the new URL with the new locale
    let newPath = location.pathname;

    // Remove current locale prefix if exists (e.g., /ur/ or /en/)
    if (currentLocale !== 'en' && newPath.startsWith(`/${currentLocale}/`)) {
      newPath = newPath.replace(`/${currentLocale}`, '') || '/';
    } else if (currentLocale === 'en' && newPath === '/') {
      // Home page
      newPath = '/';
    }

    // Add new locale prefix if not English (English is default)
    if (newLocale !== 'en') {
      newPath = `/${newLocale}${newPath}`;
    }

    // Preserve search and hash
    const searchAndHash = location.search + location.hash;

    // Navigate to new locale
    window.location.href = newPath + searchAndHash;
  };

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
