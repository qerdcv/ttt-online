import i18next from 'i18next';
import { initReactI18next } from 'react-i18next';
import Backend from 'i18next-http-backend';
import LanguageDetector from 'i18next-browser-languagedetector';

import { languages } from 'i18n/i18n.constants';
import en from 'i18n/translations/en.json';
import uk from 'i18n/translations/uk.json';

void i18next
  .use(Backend)
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    fallbackLng: languages.en,
    resources: {
      [languages.en]: {
        translation: en,
      },
      [languages.uk]: {
        translation: uk
      },
    },
  });
