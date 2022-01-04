import { Link } from 'react-router-dom';

import styles from "components/Header/header.module.scss"

export const Header = () => {
  return (
    <header className={styles.header}>
      <Link to="/" className={styles.home}>Home</Link>

      <nav className={styles.navbar}>
        <Link to="/auth/login" className={styles.navbarItem}>Sign IN</Link>/
        <Link to="/auth/register" className={styles.navbarItem}>Sign UP</Link>
      </nav>
    </header>
  )
}
