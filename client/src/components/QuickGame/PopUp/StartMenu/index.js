import { useContext } from "react";
import { Button } from "components/Button";
import { PopUpContext } from "context/popUp.context";
import { fast, createRoom, loginRoom } from "components/QuickGame/constant";
import styles from "components/QuickGame/PopUp/StartMenu/StartMenu.module.scss";

export const StartMenu = () => {
  const { onPushPopUpStack } = useContext(PopUpContext);

  return (
    <div className={styles.startMenu}>
      <Button value="Fast" classNames={[styles.startMenuButton]} onClick={onPushPopUpStack.bind(null, fast)}/>
      <Button value="Create Room" classNames={[styles.startMenuButton]} onClick={onPushPopUpStack.bind(null, createRoom)}/>
      <Button value="Login Room" classNames={[styles.startMenuButton]} onClick={onPushPopUpStack.bind(null, loginRoom)}/>
    </div>
  );
};
