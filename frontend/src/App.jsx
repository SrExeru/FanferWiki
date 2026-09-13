import { Routes, Route } from 'react-router-dom';
// Layouts
import MainLayout from './Layout/MainLayout/MainLayout.jsx';
import OnlyFormLayout from './Layout/OnlyFormLayout/OnlyFormLayout.jsx';
// Pages
import HomePage from './pages/HomePage/HomePage.jsx';
import LoginPage from './pages/LoginPage/LoginPage.jsx';
import RegisterPage from './pages/RegisterPage/RegisterPage.jsx';

function App() {
  return (
    <Routes>
      <Route element={<MainLayout />}>
        <Route path='/' element={<HomePage />}/>
      </Route>
      <Route element={<OnlyFormLayout />}>
        <Route path='/login' element={<LoginPage />}/>
        <Route path='/register' element={<RegisterPage />}/>
      </Route>
    </Routes>
  )
}

export default App;
