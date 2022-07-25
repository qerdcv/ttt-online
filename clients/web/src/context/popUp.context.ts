import { createContext } from 'react';

const noon = function () {};

export enum Stack {
  StartMenu = 'startMenu',
  Fast = 'fast',
  CreateRoom = 'createRoom',
  LoginRoom = 'loginRoom',
  ConnectRoom = 'connectRoom',
  Unauthorized = 'unauthorized',
}

interface IPopUpContext {
  // onPushPopUpStack: function (type: Stack, ctx) {};
  onPushPopUpStack(type: Stack, ctx: object): void;
  onPopPopUpStack(): void;
  resetPopUpStack(): void;
  popUpStack: Stack[];
  popUpCtx: { [key: string]: any };
}

export const PopUpContext = createContext<IPopUpContext>({
  onPushPopUpStack: function (_: Stack, ctx) {},
  onPopPopUpStack: noon,
  resetPopUpStack: noon,
  popUpStack: [],
  popUpCtx: {},
});
