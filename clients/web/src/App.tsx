import React, { useCallback, useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { MainLayout } from 'layouts/main';
import { Error } from 'layouts/Error';
import { Header } from 'components/Header';
import { Footer } from 'components/Footer';
import { GameLayout } from 'layouts/game';
import authLayout from 'layouts/auth';

import { AuthContext } from 'context/auth.context';
import { IUser } from 'types/user';
import { GameHistory } from 'layouts/history';

function App(): React.ReactElement {
  const [user, setUser] = useState<IUser | null>(null);
  const isAuthenticated = useCallback(() => !!user, [user]);

  useEffect(() => {
    const rawUser = localStorage.getItem('user');
    if (rawUser) {
      try {
        setUser(JSON.parse(rawUser) as IUser);
      } catch (e) {
        console.error(e);
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
          <Route path="games">
            <Route path=":gameID" element={<GameLayout />}/>
            <Route path=":gameID/history" element={<GameHistory />}/>
          </Route>
          <Route path="*" element={<Error code={404}/>}/>
        </Routes>
        <Footer/>
      </Router>
    </AuthContext.Provider>
  );
}

export default App;
