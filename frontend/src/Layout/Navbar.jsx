import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api.js";
import SearchIcon from '../assets/icons/SearchIcon.svg?react';
import UserIcon from '../assets/icons/userIcon.svg?react';

function Navbar() {
    // User menu

    const [showMenu, setShowMenu] = useState(false);

    const toggleMenuMode = () => setShowMenu(!showMenu);

    const [userData, setUserData] = useState(null);
    const [loggedUser, setLoggenUser] = useState(false);
    const [loadingUserData, setLoadingUserData] = useState(true);

    useEffect(() => {
        api.get('/user/@me')
            .then(response => {
                setUserData(response.data);
                setLoggenUser(true);
            })
            .catch(error => {
                console.error('Loading user data error:', error);
            })
            .finally(() => {
                setLoadingUserData(false);
            });
    }, [])

    // Search form

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
                    <input type="text" name="query" placeholder="Search communities" required={true} />
                    <button>
                        <SearchIcon className="primary_color_icon" id="header_search_btn" />
                    </button>
                </form>

                <div className="user_menu_container">
                    <button className="empty_button" onClick={toggleMenuMode}>
                        <UserIcon className="pickable_icon" />
                    </button>

                    {showMenu && (
                        <div id="user_menu_options" className="container">
                            {!loadingUserData && loggedUser ? (
                                <>
                                    <h5>{userData?.username}</h5>
                                    <ul>
                                        <li>
                                            <a href="/profile">Profile</a>
                                        </li>
                                        <li>
                                            <a href="/logout">Logout</a>
                                        </li>
                                    </ul>
                                </>
                            ) : (
                                <>
                                    <li>
                                        <a href="/login">Login</a>
                                    </li>
                                    <li>
                                        <a href="/register">Register</a>
                                    </li>
                                </>
                            )}
                        </div>
                    )}
                </div>

            </nav>
        </header>
    )
}

export default Navbar;