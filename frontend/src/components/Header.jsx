import { Link } from 'react-router-dom'

// Basic header with just a logo
function Header({isLoggedIn = false}) {
    return (
        <header>
            <Link to={isLoggedIn ? "/home" : "/"} className="logo">
                <img src="/logo.jpg" alt="Logo" />
            </Link>
        </header>
    );
}

export default Header;