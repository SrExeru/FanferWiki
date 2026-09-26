import { useState, useEffect } from "react";
import api from "../services/api.js";
import UserIcon from '../assets/icons/userIcon.svg?react';

function UserMenu () {
    const [showMenu, setShowMenu] = useState(false);

    const toggleMenuMode = () => setShowMenu(!showMenu);

    // Data
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
                console.log('Loading user data error:', error);
            })
            .finally(() => {
                setLoadingUserData(false);
            });
    }, [])

    if (loadingUserData) {
        return  (
            <div className="user_menu_container">
                <button className="empty_button" onClick={toggleMenuMode}>
                        <UserIcon className="pickable_icon" />
                </button>

                {showMenu && (
                    <div id="user_menu_options" className="container">
                        <h5>Loading...</h5>
                    </div>
                )}
            </div>
        )
    }

    if (!loggedUser) {
        return (
            <div className="user_menu_container">
                <button className="empty_button" onClick={toggleMenuMode}>
                        <UserIcon className="pickable_icon" />
                </button>

                {showMenu && (
                    <div id="user_menu_options" className="container">
                        <ul>
                            <li>
                                <a href="/login">Login</a>
                            </li>
                            <li>
                                <a href="/register">Register</a>
                            </li>
                        </ul>

                    </div>
                )}
            </div>
        )
    }

    // Future login validation

    return (
        <div className="user_menu_container">
            <button className="empty_button" onClick={toggleMenuMode}>
                    <UserIcon className="pickable_icon" />
            </button>

            {showMenu && (
                <div id="user_menu_options" className="container">
                    <h5>{ userData?.username }</h5>
                    <ul>
                        <li>
                            <a href="/profile">Profile</a>
                        </li>
                        <li>
                            <a href="/logout">Logout</a>
                        </li>
                    </ul>

                </div>
            )}
        </div>
    )
}

export default UserMenu;