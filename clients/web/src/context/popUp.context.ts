import { createContext } from 'react';

const noon = function () {};

export enum Stack {
  StartMenu = 'startMenu',
  CreateGame = 'createGame',
  LoginGame = 'loginRoom',
  Unauthorized = 'unauthorized',
}

interface IPopUpContext {
  // onPushPopUpStack: function (type: Stack, ctx) {};
  onPushPopUpStack(type: Stack, ctx: object): void;
  onPopPopUpStack(): void;
  resetPopUpStack(): void;
  popUpStack: Stack[];
  popUpCtx: { [key: string]: object };
}

export const PopUpContext = createContext<IPopUpContext>({
	onPushPopUpStack: function (_: Stack, ctx) {},
	onPopPopUpStack: noon,
	resetPopUpStack: noon,
	popUpStack: [],
	popUpCtx: {},
});
