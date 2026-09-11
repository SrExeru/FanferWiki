import { Routes, Route } from 'react-router-dom';
// Layouts
import MainLayout from './Layout/MainLayout';
import OnlyFormLayout from './Layout/OnlyFormLayout';
// Pages
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';

function App() {
  return (
    <Routes>
      <Route element={<MainLayout />}>
        <Route path='/' element={<HomePage />}/>
      </Route>
      <Route element={<OnlyFormLayout />}>
        <Route path='/login' element={<LoginPage />}/>
      </Route>
    </Routes>
  )
}

export default App;
