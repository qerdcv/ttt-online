import React from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

import styles from 'components/QuickGame/PopUp/Unauthorized/unauthorized.module.scss';


export const Unauthorized = () => {
  const { t } = useTranslation();
  return (
    <div className={styles.unauthorized}>
      <h1>{ t`To play, you must be Authorized!`}</h1>
      <div>
        <Link to="/auth/login" className={styles.unauthorizedLink}>{ t`Sign IN`}</Link>/
        <Link to="/auth/register" className={styles.unauthorizedLink}>{ t`Sign UP` }</Link>
      </div>
    </div>
  );
};
