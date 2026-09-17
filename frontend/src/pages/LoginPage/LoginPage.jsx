import { useState } from 'react';
import api from '../../services/api.js';
import './LoginPage.css';

function LoginPage() {
    const [loginError, setLoginError] = useState(null);

    const handleLogin = async (e) => {
        e.preventDefault();

        const form = e.target;
        const formData = new FormData(form);

        try {
            const access_token = await api.post('/auth/login', formData);
            localStorage.setItem('access_token', access_token.data)
            console.log(access_token.data);
        } catch (error) {
            setLoginError(error)
            console.log('Login error:', error);
        }
    };

    return (
        <>
            <h1>Login</h1>
            <form onSubmit={handleLogin}>
                <div className="form_question">
                    <label htmlFor="email">Email</label>
                    <input type="email" name="email" id="email" required={true}/>
                </div>

                <div className="form_question">
                    <label htmlFor="password">Password</label>
                    <input type="password" name="password" id="password" required={true}/>
                </div>
                
                <input type="submit" value="Login" />
            </form>
            <p>{loginError}</p>
        </>
    )
}

export default LoginPage;