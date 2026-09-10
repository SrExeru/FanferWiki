import './CommunityCard.css'

function CommunityCard({ display_name, icon_url, description }) {
    return (
        <div className='community_card'>
            <img src={ icon_url } alt={`${display_name}'s logo`} />
            <h3>
                { display_name }
            </h3>
            <p>
                { description }
            </p>
        </div>
    )
}

export default CommunityCard