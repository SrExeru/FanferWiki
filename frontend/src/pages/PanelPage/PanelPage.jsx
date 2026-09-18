import { useState } from "react";
import api from "../../services/api";

function PanelPage() {
    const [userInfo, setUserInfo] = useState(null);
    const [loadingUserInfo, setLoadingUserInfo] = useState(true);

    api.get('/user/@me')
        .then(response => {
            setUserInfo(response.data)
        })
        .catch(error => {
            console.error('Loading user data error:', error)
        })
        .finally(() => {
            setLoadingUserInfo(false)
        });

    if (loadingUserInfo) {
        return <p>Loading...</p>
    }

    return (
        <>
            <h1>Welcome { userInfo?.username }</h1>
        </>
    )
}

export default PanelPage;