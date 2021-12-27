import { Header } from "components/Header";
import { Footer } from "components/Footer";
import { QuickGame } from "components/QuickGame";

import { PopUpContext } from "context/popUp.context";
import { useState } from "react";

export const MainLayout = () => {
  const [popUpStack, setPopUpStack] = useState([]);

  const onPushPopUpStack = (popUpType) => {

    setPopUpStack((prevStack) => {
      return [...prevStack, popUpType];
    });
  };

  const onPopPopUpStack = () => {
    setPopUpStack((prevStack) => {
      return prevStack.slice(0, prevStack.length - 1);
    });
  };

  const resetPopUpStack = () => {
    setPopUpStack([]);
  }

  return (
    <>
      <Header/>
      <PopUpContext.Provider value={{
        onPushPopUpStack,
        onPopPopUpStack,
        resetPopUpStack,
        popUpStack
      }}>
        <QuickGame/>
      </PopUpContext.Provider>
      <Footer/>
    </>
  );
};
