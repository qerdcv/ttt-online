import { createContext } from "react";



export const PopUpContext = createContext({
  onPushPopUpStack: function (type, ctx){},
  onPopPopUpStack: function (){},
  resetPopUpStack: function (){},
  popUpStack: [],
  popUpCtx: {}
})
