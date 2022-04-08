import { QuickGame } from 'components/QuickGame';

import { PopUpContext, Stack } from 'context/popUp.context';
import { useState } from 'react';

export const MainLayout = () => {
  const [popUpStack, setPopUpStack] = useState<Stack[]>([]);
  const [popUpCtx, setPopUpCtx] = useState({});

  const onPushPopUpStack = (type: Stack, ctx = {}) => {
    setPopUpCtx(ctx);
    setPopUpStack((prevStack: Stack[]) => {
      return [...prevStack, type];
    });
  };

  const onPopPopUpStack = () => {
    setPopUpStack((prevStack) => {
      return prevStack.slice(0, prevStack.length - 1);
    });
  };

  const resetPopUpStack = () => {
    setPopUpStack([]);
  };

  return (
    <PopUpContext.Provider
      value={{
        onPushPopUpStack,
        onPopPopUpStack,
        resetPopUpStack,
        popUpStack,
        popUpCtx,
      }}
    >
      <QuickGame />
    </PopUpContext.Provider>
  );
};
