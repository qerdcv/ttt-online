import React, { useState } from 'react';
import { changeLanguage } from 'i18next';
import { useTranslation } from 'react-i18next';

import { languages } from 'i18n/i18n.constants';
import styles from 'components/LanguageSwitcher/languageSwitch.module.scss';

const flags = {
  [languages.en]: '🇬🇧',
  [languages.uk]: '🇺🇦',
};

const names = {
  [languages.en]: 'English',
  [languages.uk]: 'Українська',
};

export const LanguageSwitcher = () => {
  const [isActive, setIsActive] = useState(false);
  const { i18n: { language } } = useTranslation();

  return (
    <div className={styles.languageSwitcher} onClick={() => setIsActive(!isActive)}>
      <span>{ flags[language] || flags[languages.en] }</span>&nbsp;
      <h3 className={isActive ? styles.arrowActive : ''}>▼</h3>
      <div className={`${styles.dropdown} ${isActive ? styles.dropdownActive : ''}`}>
        {Object.keys(languages).map((lg) => {
          return (
            <div className={styles.dropdownItem} key={`lang-${lg}`} onClick={() => changeLanguage(lg)}>
              {flags[lg]}&nbsp;{names[lg]}
            </div>
          );
        })}
      </div>
    </div>
  );
};
