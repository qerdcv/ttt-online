import { createContext } from 'react';
import { User } from 'types/user';

interface IAuthContext {
    isAuthenticated: boolean,
    user: User

    setIsAuthenticated: (isAuthenticated: boolean) => void;
    setUser: (user: User) => void,
}

export const AuthContext = createContext<IAuthContext>({
    isAuthenticated: false,
    user: {},

    setIsAuthenticated(_) {},
    setUser(_) {}
});
