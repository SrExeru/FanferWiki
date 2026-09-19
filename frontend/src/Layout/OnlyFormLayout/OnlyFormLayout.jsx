import { Outlet } from 'react-router-dom';
import Navbar from '../Navbar.jsx';
import Footer from "../Footer";
import './OnlyFormLayout.css'

function OnlyFormLayout() {
    return (
        <>
            <Navbar />

            <main className='container'>
                <Outlet />
            </main>

            <Footer />
        </>
    )
}

export default OnlyFormLayout;