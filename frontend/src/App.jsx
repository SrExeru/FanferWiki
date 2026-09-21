import { Routes, Route } from 'react-router-dom';
// Layouts
import MainLayout from './Layout/MainLayout/MainLayout.jsx';
import OnlyFormLayout from './Layout/OnlyFormLayout/OnlyFormLayout.jsx';
import SearchLayout from './Layout/SearchLayout/SearchLayout.jsx';
// Pages
import HomePage from './pages/HomePage/HomePage.jsx';
import LoginPage from './pages/LoginPage/LoginPage.jsx';
import RegisterPage from './pages/RegisterPage/RegisterPage.jsx';
import PanelPage from './pages/PanelPage/PanelPage.jsx';
import SearchPage from './pages/SearchPage/SearchPage.jsx';
import CommunityPage from './pages/CommunityPage/CommunityPage.jsx';
import ProfilePage from './pages/ProfilePage/ProfilePage.jsx';

function App() {
  return (
    <Routes>
      <Route element={<MainLayout />}>
        <Route path='/' element={<HomePage />}/>
        <Route path='/panel' element={<PanelPage />}/>
        <Route path='/community/:slug' element={<CommunityPage /> } />
        <Route path='/profile' element={<ProfilePage /> } />
      </Route>

      <Route element={<SearchLayout />}>
        <Route path='/search' element={<SearchPage />} />
      </Route>

      <Route element={<OnlyFormLayout />}>
        <Route path='/login' element={<LoginPage />}/>
        <Route path='/register' element={<RegisterPage />}/>
      </Route>
    </Routes>
  )
}

export default App;
