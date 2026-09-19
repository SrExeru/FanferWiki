import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import CommunityCard from '../../components/CommunityCard/CommunityCard';
import api from '../../services/api';
import './SearchPage.css';

function SearchPage () {
    const [searchParams] = useSearchParams();
    const queryText = searchParams.get('query');
    
    const [searchResults, setSearchResults] = useState(null);
    const [LoadingSearchResults, setLoadingSearchResults] = useState(true);

    useEffect(() => {
        api.get(`/community/search?query=${queryText}`)
            .then(response => {
                setSearchResults(response.data);
            })
            .catch(error => {
                console.error('Search error:', error);
            })
            .finally(() => {
                setLoadingSearchResults(false)
            });
    }, []);

    if (LoadingSearchResults) {
        return <p>Loading... </p>
    } else if (!searchResults) {
        return <p>Community not found...</p>
    }

    return (
        <>
            <div className='community_list'>
            {
                searchResults.map((community) => {
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

export default SearchPage;