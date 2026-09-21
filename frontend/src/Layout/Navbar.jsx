import { useNavigate } from "react-router-dom";
import UserMenu from "./UserMenu.jsx";
import SearchIcon from '../assets/icons/SearchIcon.svg?react';

function Navbar () {
    const navigate = useNavigate();

    const handleSearch = (e) => {
        e.preventDefault();
        
        const form = e.target;
        const formData = new FormData(form);

        const query = formData.get('query');

        navigate(`/search?query=${query}`);
        window.location.reload();
    };

    return (
        <header>
            <a href="/" className='header_logo'>
                <img src="/logo.png" alt="Fafner Wiki Logo" />
                <span>
                    FafnerWiki
                </span>
            </a>

            <nav>
                <form className="nav_search" onSubmit={handleSearch}>
                    <input type="text" name="query" placeholder="Search communities" required={true}/>
                    <button>
                        <SearchIcon className="primary_color_icon" id="header_search_btn" />
                    </button>
                </form>
                
                <UserMenu />

            </nav>
        </header>
    )
}

export default Navbar;