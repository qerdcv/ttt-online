import React, { useContext } from 'react';
import { Button } from 'components/Button';
import { PopUpContext, Stack } from 'context/popUp.context';

import styles from 'components/QuickGame/PopUp/StartMenu/StartMenu.module.scss';

export const StartMenu = () => {
  const { onPushPopUpStack } = useContext(PopUpContext);

  return (
    <div className={styles.startMenu}>
      <Button
        value="Create Game"
        classNames={[styles.startMenuButton]}
        onClick={onPushPopUpStack.bind(null, Stack.CreateGame)}
      />
      <Button
        value="Login Game"
        classNames={[styles.startMenuButton]}
        onClick={onPushPopUpStack.bind(null, Stack.LoginGame)}
      />
    </div>
  );
};
