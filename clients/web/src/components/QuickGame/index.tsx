import React, { useContext, useMemo } from 'react';
import { Button } from 'components/Button';
import { PopUp } from 'components/PopUp';
import {
  StartMenu,
  LoginRoom,
  CreateRoom,
  Fast,
  ConnectRoom,
  Unauthorized,
} from 'components/QuickGame/PopUp';
import { PopUpContext, Stack } from 'context/popUp.context';
import { AuthContext } from 'context/auth.context';

import styles from 'components/QuickGame/quick.module.scss';

export const QuickGame = (): React.ReactElement => {
  const { isAuthenticated } = useContext(AuthContext);
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
      [Stack.Unauthorized]: <Unauthorized />,
    };
  }, []);

  return (
    <main className={styles.main}>
      <h1 className={styles.mainTitle}>Quick Game</h1>
      <Button
        value="Play !"
        classNames={[styles.mainBtn]}
        onClick={ isAuthenticated
            ? onPushPopUpStack.bind(null, Stack.StartMenu)
            : onPushPopUpStack.bind(null, Stack.Unauthorized)}
      />
      {popUpStack.length !== 0 && (
        <PopUp closeEvent={resetPopUpStack}>
          {popUps[popUpStack[popUpStack.length - 1]]}
        </PopUp>
      )}
    </main>
  );
};
