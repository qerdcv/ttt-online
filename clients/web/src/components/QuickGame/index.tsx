import React, { useContext, useMemo } from 'react';
import { Button } from 'components/Button';
import { PopUp } from 'components/PopUp';
import {
  StartMenu,
  LoginRoom,
  CreateRoom,
  Fast,
  ConnectRoom,
} from 'components/QuickGame/PopUp';
import { PopUpContext, Stack } from 'context/popUp.context';
import styles from 'components/QuickGame/quick.module.scss';

export const QuickGame = (): React.ReactElement => {
  const { popUpStack, resetPopUpStack, onPushPopUpStack } =
    useContext(PopUpContext);

  const popUps = useMemo<{ [key in Stack]: React.ReactElement }>((): {
    [key in Stack]: React.ReactElement;
  } => {
    return {
      [Stack.StartMenu]: <StartMenu />,
      [Stack.CreateRoom]: <CreateRoom />,
      [Stack.LoginRoom]: <LoginRoom />,
      [Stack.ConnectRoom]: <ConnectRoom />,
      [Stack.Fast]: <Fast />,
    };
  }, []);

  return (
    <main className={styles.main}>
      <h1 className={styles.mainTitle}>Quick Game</h1>
      <Button
        value="Play !"
        classNames={[styles.mainBtn]}
        onClick={onPushPopUpStack.bind(null, Stack.StartMenu)}
      />
      {popUpStack.length !== 0 && (
        <PopUp closeEvent={resetPopUpStack}>
          {popUps[popUpStack[popUpStack.length - 1]]}
        </PopUp>
      )}
    </main>
  );
};
