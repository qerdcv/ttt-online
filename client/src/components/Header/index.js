import styles from "components/Header/header.module.scss"

export const Header = () => {
    return (
        <header className={styles.header}>
            <nav className={styles.navbar}>
              <a href="#" className={styles.navbarItem}>Sign IN</a>/
              <a href="#" className={styles.navbarItem}>Sign UP</a>
            </nav>
        </header>
    )
}
