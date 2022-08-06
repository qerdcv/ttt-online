import { createContext } from 'react';
import { IUser } from 'types/user';

export interface IAuthContext {
    user: IUser | null
    isAuthenticated: () => boolean,
    setUser: (user: IUser | null) => void,
}

export const AuthContext = createContext<IAuthContext>({
  user: null,
  isAuthenticated: () => false,
  setUser: (_) => {}
});
