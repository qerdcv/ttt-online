import { createContext } from 'react';
import { User } from 'types/user';

interface IAuthContext {

    user: User
    isAuthenticated: () => boolean,
    setUser: (user: User) => void,
}

export const AuthContext = createContext<IAuthContext>({
    user: {},

    isAuthenticated: () => false,
    setUser(_) {}
});
