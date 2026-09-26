import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api.js';

function LogoutPage () {
    const navigate = useNavigate();

    localStorage.removeItem('access_token');

    useEffect(() => {
        api.post('/auth/logout')
            .then(response => {
                localStorage.removeItem('access_token');
                navigate('/');
            })  
            .catch (error => {
                console.log('Logout error:', error);
            });
    }, []);

    return (
        <>
            Starting logout...
        </>
    )
}

export default LogoutPage;