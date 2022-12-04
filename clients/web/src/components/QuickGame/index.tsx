import React, { useContext, useMemo } from 'react';
import { useTranslation } from 'react-i18next';
import { Button } from 'components/Button';
import { PopUp } from 'components/PopUp';
import {
  StartMenu,
  LoginGame,
  CreateGame,
  Unauthorized,
} from 'components/QuickGame/PopUp';
import { PopUpContext, Stack } from 'context/popUp.context';
import { AuthContext } from 'context/auth.context';

import styles from 'components/QuickGame/quick.module.scss';

export const QuickGame = (): React.ReactElement => {
  const { t } = useTranslation();
  const { isAuthenticated } = useContext(AuthContext);
  const { popUpStack, resetPopUpStack, onPushPopUpStack } =
    useContext(PopUpContext);

  const popUps = useMemo<{[key in Stack]: React.ReactElement}>((): {
    [key in Stack]: React.ReactElement;
  } => {
    return {
      [Stack.StartMenu]: <StartMenu />,
      [Stack.CreateGame]: <CreateGame />,
      [Stack.LoginGame]: <LoginGame />,
      [Stack.Unauthorized]: <Unauthorized />,
    };
  }, []);

  return (
    <main className={styles.main}>
      <h1 className={styles.mainTitle}>{ t`Quick Game` }</h1>
      <Button
        value='Play !'
        classNames={[styles.mainBtn]}
        onClick={ isAuthenticated()
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
