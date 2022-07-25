import React, { useCallback, useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { MainLayout } from 'layouts/main';
import { Error } from 'layouts/Error';
import { Header } from 'components/Header';
import { Footer } from 'components/Footer';
import { GameLayout } from 'layouts/game';
import authLayout from 'layouts/auth';

import { AuthContext } from 'context/auth.context';
import { User } from 'types/user';

function App(): React.ReactElement {
    const [user, setUser] = useState<User>({});
    const isAuthenticated = useCallback(() => !!Object.keys(user).length, [user]);

    useEffect(() => {
        let rawUser = localStorage.getItem("user")
        if (rawUser) {
            try {
                setUser(JSON.parse(rawUser))
            } catch (e) {
                console.error(e)
            }
        }
    }, [setUser]);

    return (
        <AuthContext.Provider value={{
            user,
            isAuthenticated,
            setUser,
        }}>
            <Router>
                <Header/>
                <Routes>
                    <Route index element={<MainLayout/>}/>
                    <Route path="auth">
                        <Route path="login" element={<authLayout.Login />} />
                        <Route path="register" element={<authLayout.Register />} />
                    </Route>
                    <Route path="/games/:gameID" element={<GameLayout />}/>
                    <Route path="*" element={<Error code={404}/>}/>
                </Routes>
                <Footer/>
            </Router>
        </AuthContext.Provider>
    );
}

export default App;
