import React, { useContext } from 'react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';

import { AuthContext } from 'context/auth.context';
import { useHttp } from 'hooks/useHttp';
import { Auth } from 'api/auth';
import { LanguageSwitcher } from 'components/LanguageSwitcher';

import styles from 'components/Header/header.module.scss';


export const Header = () => {
  const { t } = useTranslation();
  const { isAuthenticated, setUser } = useContext(AuthContext);
  const { request } = useHttp();
  const logout = () => {
    request(Auth.logout)
      .then(() => {
        setUser(null);
        localStorage.removeItem('user');
      })
      .catch(console.error);
  };

  return (
    <header className={styles.header}>
      <Link to="/" className={styles.home}>TTTO</Link>

      <nav className={styles.navbar}>
        <LanguageSwitcher />
        {isAuthenticated()
          ? <span onClick={logout} className={styles.navbarItem}>{t`Logout`}</span>
          : (
            <>
              <Link to="/auth/login" className={styles.navbarItem}>{t`Sign IN`}</Link>/
              <Link to="/auth/register" className={styles.navbarItem}>{t`Sign UP`}</Link>
            </>
          )}
      </nav>
    </header>
  );
};
