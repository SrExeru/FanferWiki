import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import api from '../../services/api';
import './CommunityPage.css'

function CommunityPage () {
    const searchParams = useParams();
    const communitySlug = searchParams.slug;

    // Community data loading
    const [CommunityData, setCommunityData] = useState(null);
    const [LoadingCommunityData, setLoadingCommunityData] = useState(true);

    useEffect(() => {
        api.get(`/community/${communitySlug}`)
            .then(response => {
                setCommunityData(response.data);
            })
            .catch(error => {
                console.error('Community loading:', error);
            })
            .finally(() => {
                setLoadingCommunityData(false);
            });
    }, []);

    if (LoadingCommunityData) {
        return <p>Loading...</p>
    }

    return (
        <>
            <h1>{ CommunityData?.display_name }</h1>
            <img src={CommunityData?.icon_url} alt={`${CommunityData?.display_name}'s icon`} className='community_icon'/>
            <p>{ CommunityData?.description }</p>
        </>
    )
}

export default CommunityPage;