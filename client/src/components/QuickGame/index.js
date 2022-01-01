import { useContext, useMemo } from "react";
import { Button } from "components/Button";
import { PopUp } from "components/PopUp";
import { StartMenu, LoginRoom, CreateRoom, Fast } from "components/QuickGame/PopUp";
import { startMenu, loginRoom, createRoom, fast } from "components/QuickGame/constant";
import { PopUpContext } from "context/popUp.context";
import styles from 'components/QuickGame/quick.module.scss';

export const QuickGame = () => {
  const {popUpStack, resetPopUpStack, onPushPopUpStack} = useContext(PopUpContext);

  const popUps = useMemo(() => {
    return {
      [startMenu]: <StartMenu/>,
      [createRoom]: <CreateRoom/>,
      [loginRoom]: <LoginRoom/>,
      [fast]: <Fast />,
    };
  }, []);

  return (
    <main className={styles.main}>
      <h1 className={styles.mainTitle}>Quick Game</h1>
      <Button value="Play !" classNames={[styles.mainBtn]} onClick={onPushPopUpStack.bind(null, startMenu)}/>
      {popUpStack.length !== 0 && (
        <PopUp closeEvent={resetPopUpStack}>
          {popUps[popUpStack[popUpStack.length - 1]]}
        </PopUp>
      )}
    </main>
  );
};
