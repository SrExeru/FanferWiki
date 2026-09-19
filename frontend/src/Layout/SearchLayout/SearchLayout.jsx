import { Outlet, useSearchParams } from "react-router-dom";
import Navbar from "../Navbar";
import Footer from "../Footer";
import './SearchLayout.css';

function SearchLayout () {
    const [searchParams] = useSearchParams();

    return (
        <>
            <Navbar />

            <main className='container main_full_screen'>
                <h1>Results for '{searchParams.get('query')}'</h1>
                <Outlet />
            </main>

            <Footer />
        </>
    )
}

export default SearchLayout;