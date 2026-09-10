import { useState, useEffect } from 'react';
import CommunityCard from '../../components/CommunityCard';
import api from '../../services/api.js';
import './HomePage.css';

function HomePage () {
    const [communitiesLoading, setCommunitiesLoading] = useState(true);
    const [communities, setCommunities] = useState(null)

    useEffect(() => {
        api.get('/community/popular')
            .then(response => {
                console.log(response?.data)
                setCommunities(response?.data)
            })
            .catch(error => {
                console.error(error)
            })
            .finally(() => {
                setCommunitiesLoading(false);
            });

    }, []);

    if (communitiesLoading) {
        return <p>Loading...</p>
    }

    console.log('-', communities)

    return (
        <>
            <h1>Welcome to FafnerWiki</h1>
            <div className='community_list'>
                {
                    communities.map((community) => {
                        return <CommunityCard
                            key={community?.id}
                            display_name={community?.display_name}
                            description={community?.description}
                            icon_url={community?.icon_url}
                        />
                    })
                }
            </div>
        </>
    )
}

export default HomePage;