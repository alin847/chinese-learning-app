import { Link } from 'react-router-dom'
import SearchBar from './SearchBar'
import AccountMenu from './AccountMenu'


// Header component with search bar and logout functionality (use for home page)
function HeaderHome() {
return (
    <header>
        <Link to={"/home"} className="logo">
            <img src="/logo.jpg" alt="Logo" />
        </Link>

        <SearchBar />

        <AccountMenu />

    </header>
)
}

export default HeaderHome;
