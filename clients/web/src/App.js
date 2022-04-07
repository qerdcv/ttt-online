import { BrowserRouter as Router, Route, Routes} from "react-router-dom";
import { MainLayout } from "layouts/main";
import { Error } from "layouts/Error";
import { Header } from "components/Header";
import { Footer } from "components/Footer";

function App() {
  return (
    <Router>
      <Header/>
      <Routes>
        <Route path="/" element={<MainLayout />} />
        {/*TODO: Investigate hot to create nested routes in v6 react-router-dom*/}
        <Route path="/auth/login" element={<h1>Login page</h1>}/>
        <Route path="/auth/register" element={<h1>Register page</h1>} />
        <Route path="*" element={<Error code={404} />}/>
      </Routes>
      <Footer/>
    </Router>
  );
}

export default App;
