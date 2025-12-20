/**
 * Language Toggle Component
 * Switches between English and Urdu with smooth transitions
 */
import React from 'react';
import { useLanguage, Language } from '@site/src/i18n';
import './styles.css';

export function LanguageToggle() {
  const { language, setLanguage } = useLanguage();

  const toggleLanguage = () => {
    const newLang: Language = language === 'en' ? 'ur' : 'en';
    setLanguage(newLang);
  };

  return (
    <button
      onClick={toggleLanguage}
      className="language-toggle"
      title={language === 'en' ? 'اردو میں تبدیل کریں' : 'Switch to English'}
      aria-label={language === 'en' ? 'Switch to Urdu' : 'Switch to English'}
    >
      <span className="language-toggle-icon">
        {language === 'en' ? '🇵🇰' : '🇬🇧'}
      </span>
      <span className="language-toggle-text">
        {language === 'en' ? 'اردو' : 'EN'}
      </span>
    </button>
  );
}

// Alternative: Dropdown style toggle
export function LanguageDropdown() {
  const { language, setLanguage } = useLanguage();

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setLanguage(e.target.value as Language);
  };

  return (
    <select
      value={language}
      onChange={handleChange}
      className="language-dropdown"
      aria-label="Select language"
    >
      <option value="en">English</option>
      <option value="ur">اردو</option>
    </select>
  );
}

// Pill-style toggle
export function LanguagePillToggle() {
  const { language, setLanguage } = useLanguage();

  return (
    <div className="language-pill-toggle">
      <button
        onClick={() => setLanguage('en')}
        className={`language-pill ${language === 'en' ? 'active' : ''}`}
      >
        EN
      </button>
      <button
        onClick={() => setLanguage('ur')}
        className={`language-pill ${language === 'ur' ? 'active' : ''}`}
      >
        اردو
      </button>
    </div>
  );
}

export default LanguageToggle;
