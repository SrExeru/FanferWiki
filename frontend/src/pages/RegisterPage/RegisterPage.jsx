import { useState } from 'react';
import api from '../../services/api.js';
import './RegisterPage.css'

function RegisterPage() {
    const [registerError, setRegisterError] = useState(null);

    const HandleRegisterForm = async (e) => {
        e.preventDefault();

        const form = e.target;
        const formData = new FormData(form);

        try {
            const access_token = await api.post('/auth/register', formData);
            console.log(access_token.data);
        } catch (e) {
            console.error('Register error:', e);
            setRegisterError(e)
        }
    };


    return (
        <>
            <h1>Register</h1>
            <form onSubmit={HandleRegisterForm}>
                <div className="form_question">
                    <label htmlFor="username">Username</label>
                    <input type="text" name="username" id="username" required={true}/>
                </div>
                <div className="form_question">
                    <label htmlFor="email">Email</label>
                    <input type="email" name="email" id="email" required={true}/>
                </div>
                <div className="form_question">
                    <label htmlFor="password">Password</label>
                    <input type="password" name="password" id="password"  required={true}/>
                </div>

                <input type="submit" value="Register" />
            </form>
            <p>{registerError ?? ''}</p>
        </>
    )
}

export default RegisterPage;