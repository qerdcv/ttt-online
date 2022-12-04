import React from 'react';
import { createRoot } from 'react-dom/client';
import './index.scss';
import App from 'App';
import reportWebVitals from './reportWebVitals';
import 'i18n/i18n';

createRoot(
  // eslint-disable-next-line
  document.getElementById('root')!,
).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
