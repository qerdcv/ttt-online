import { createContext } from 'react';
import { IUser } from 'types/user';

export interface IAuthContext {
    user: IUser
    isAuthenticated: () => boolean,
    setUser: (user: IUser) => void,
}

export const AuthContext = createContext<IAuthContext>({
  user: {},

  isAuthenticated: () => false,
  setUser: (_) => {}
});
