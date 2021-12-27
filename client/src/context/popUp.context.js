import { createContext } from "react";



export const PopUpContext = createContext({
  onPushPopUpStack: function (popupType){},
  onPopPopUpStack: function (){},
  resetPopUpStack: function (){},
  popUpStack: []
})
