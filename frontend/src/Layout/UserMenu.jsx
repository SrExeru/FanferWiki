import { useState } from "react";

import UserIcon from '../assets/icons/userIcon.svg?react';

function UserMenu () {
    const [showMenu, setShowMenu] = useState(false);

    const toggleMenuMode = () => setShowMenu(!showMenu);

    // Future login validation

    return (
        <div className="user_menu_container">
            <button className="empty_button" onClick={toggleMenuMode}>
                    <UserIcon className="pickable_icon" />
            </button>

            {showMenu && (
                <div id="user_menu_options" className="container">
                    <h5>Options</h5>
                    <ul>
                        <li>
                            <a href="/profile">Profile</a>
                        </li>
                    </ul>

                </div>
            )}
        </div>
    )
}

export default UserMenu;