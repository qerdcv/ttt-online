import React, { useContext } from 'react';
import { Link } from 'react-router-dom';

import styles from 'components/Header/header.module.scss';
import { AuthContext } from 'context/auth.context';
import { useHttp } from 'hooks/useHttp';
import { Auth } from 'api/auth';

export const Header = () => {
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
      <Link to="/" className={styles.home}>Home</Link>

      <nav className={styles.navbar}>
        {isAuthenticated()
          ? <span onClick={logout} className={styles.navbarItem}>Logout</span>
          : (
            <>
              <Link to="/auth/login" className={styles.navbarItem}>Sign IN</Link>/
              <Link to="/auth/register" className={styles.navbarItem}>Sign UP</Link>
            </>
          )}
      </nav>
    </header>
  );
};
