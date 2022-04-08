import { useContext } from 'react';
import { Button } from 'components/Button';
import { PopUpContext, Stack } from 'context/popUp.context';
import styles from 'components/QuickGame/PopUp/StartMenu/StartMenu.module.scss';

export const StartMenu = () => {
  const { onPushPopUpStack } = useContext(PopUpContext);

  return (
    <div className={styles.startMenu}>
      <Button
        value="Fast"
        classNames={[styles.startMenuButton]}
        onClick={onPushPopUpStack.bind(null, Stack.Fast)}
      />
      <Button
        value="Create Room"
        classNames={[styles.startMenuButton]}
        onClick={onPushPopUpStack.bind(null, Stack.CreateRoom)}
      />
      <Button
        value="Login Room"
        classNames={[styles.startMenuButton]}
        onClick={onPushPopUpStack.bind(null, Stack.LoginRoom)}
      />
    </div>
  );
};
