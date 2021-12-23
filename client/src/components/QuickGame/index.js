import styles from 'components/QuickGame/quick.module.scss';
import { Button } from "../Button";

export const QuickGame = () => {
  return (
    <main className={styles.main}>
      <h1 className={styles.mainTitle}>Quick Game</h1>
      <Button value="Play !"/>
    </main>
  )
}
