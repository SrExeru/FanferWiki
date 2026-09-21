import { useEffect, useState } from "react";
import api from "../../services/api";

function ProfilePage () {
    const [profileData, setProfileData] = useState(null);
    const [loadingProfileData, setLoadingProfileData] = useState(true);

    useEffect(() => {
        api.get('/user/@me')
            .then(response => {
                setProfileData(response.data);
            })
            .catch(error => {
                console.error('Loading profile error:', error)
            })
            .finally(() => {
                setLoadingProfileData(false);
            })
    }, []);

    if (loadingProfileData) {
        return <p>Loading...</p>
    }

    return (
        <>
            <h1>Welcome { profileData?.username }</h1>
            <h2>id</h2>
            <p>{ profileData?.id }</p>
        </>
    )
}

export default ProfilePage;