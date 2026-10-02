import { createContext, useContext, useState, useEffect } from "react";
import api from "../services/api";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api.get('/user/@me')
            .then(response => {
                setUser(response.data);
            })
            .catch(error => {
                setUser(null);
            })
            .finally(() => {
                setLoading(false);
            });
    }, [])

    return (
        <AuthContext.Provider value={{ user, isAuth: !!user, loading }}>
            { children }
        </AuthContext.Provider>
    );
}

export const useAuth = () => useContext(AuthContext);