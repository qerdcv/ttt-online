import styles from 'components/QuickGame/PopUp/Unauthorized/unauthorized.module.scss';
import { Link } from 'react-router-dom';

export const Unauthorized = () => {
    return (
        <div className={styles.unauthorized}>
            <h1>To play, you must be Authorized!</h1>
            <div>
                <Link to="/auth/login" className={styles.unauthorizedLink}>Sign IN</Link>/
                <Link to="/auth/register" className={styles.unauthorizedLink}>Sign UP</Link>
            </div>
        </div>
    )
};
