import { useNavigate } from "react-router-dom";

function Navbar () {
    const navigate = useNavigate();

    const handleSearch = (e) => {
        e.preventDefault();
        
        const form = e.target;
        const formData = new FormData(form);

        const query = formData.get('query');

        navigate(`/search?query=${query}`);
        window.location.reload();
    };

    return (
        <header>
            <div className='header_logo'>
                <img src="/logo.png" alt="Fafner Wiki Logo" />
                <span>
                    FafnerWiki
                </span>
            </div>

            <form className="nav_search" onSubmit={handleSearch}>
                <input type="text" name="query" placeholder="Search communities" required={true}/>
                <input type="submit" value="🔎" />
            </form>
            
        </header>
    )
}

export default Navbar;