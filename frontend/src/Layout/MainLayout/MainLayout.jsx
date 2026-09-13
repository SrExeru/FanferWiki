import { Outlet } from 'react-router-dom';
import './MainLayout.css'

function MainLayout() {
    return (
        <>
            <header>
                <div className='header_logo'>
                    <img src="/logo.png" alt="Fafner Wiki Logo" />
                    <span>
                    FafnerWiki
                    </span>
                </div>
            </header>

            <main className='container main_full_screen'>
                <Outlet />
            </main>

            <footer>
                <div>Header icon made by <a href="https://www.flaticon.es/autores/iconfield" title="iconfield"> iconfield </a> from <a href="https://www.flaticon.es/" title="Flaticon">www.flaticon.es</a></div>
            </footer>
        </>
    )
}

export default MainLayout;