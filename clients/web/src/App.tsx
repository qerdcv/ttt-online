import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { MainLayout } from 'layouts/main';
import { Error } from 'layouts/Error';
import { Header } from 'components/Header';
import { Footer } from 'components/Footer';

import { AuthContext } from 'context/auth.context';
import { User } from 'types/user';

function App(): React.ReactElement {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [user, setUser] = useState<User>({});

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
            isAuthenticated,
            user,
            setIsAuthenticated,
            setUser,
        }}>
            <Router>
                <Header/>
                <Routes>
                    <Route index element={<MainLayout/>}/>
                    <Route path="auth">
                        <Route path="login" element={<h1>Login page</h1>} />
                        <Route path="register" element={<h1>Register page</h1>} />
                    </Route>
                    <Route path="*" element={<Error code={404}/>}/>
                </Routes>
                <Footer/>
            </Router>
        </AuthContext.Provider>
    );
}

export default App;
