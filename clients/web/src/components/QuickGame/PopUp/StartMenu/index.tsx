import React, { useContext } from 'react';
import { useTranslation } from 'react-i18next';
import { Button } from 'components/Button';
import { PopUpContext, Stack } from 'context/popUp.context';

import styles from 'components/QuickGame/PopUp/StartMenu/StartMenu.module.scss';

export const StartMenu = () => {
  const { t } = useTranslation();
  const { onPushPopUpStack } = useContext(PopUpContext);

  return (
    <div className={styles.startMenu}>
      <Button
        value={t`Create Game`}
        classNames={[styles.startMenuButton]}
        onClick={onPushPopUpStack.bind(null, Stack.CreateGame)}
      />
      <Button
        value={t`Login Game`}
        classNames={[styles.startMenuButton]}
        onClick={onPushPopUpStack.bind(null, Stack.LoginGame)}
      />
    </div>
  );
};
