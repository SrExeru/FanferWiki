import { useState, useEffect } from 'react';
import api from '../../services/api.js';
import './LoginPage.css';

function LoginPage () {
    return (
        <>
            <h1>Login</h1>
            <form action="">
                <div className="form_question">
                    <label htmlFor="email">Email</label>
                    <input type="text" name="email" id="email" required={true}/>
                </div>

                <div className="form_question">
                    <label htmlFor="email">Password</label>
                    <input type="password" name="password" id="password" required={true}/>
                </div>
                
                <input type="submit" value="Login" />
            </form>
        </>
    )
}

export default LoginPage;