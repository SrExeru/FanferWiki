import { Outlet } from 'react-router-dom';
import Navbar from '../Navbar';
import Footer from "../Footer";
import './MainLayout.css'

function MainLayout() {
    return (
        <>
            <Navbar />

            <main className='container main_full_screen'>
                <Outlet />
            </main>

            <Footer />
        </>
    )
}

export default MainLayout;