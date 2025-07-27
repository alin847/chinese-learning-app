import { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchAPI_JSON } from '../utils/api';
import './AccountMenu.css'; // Import your CSS styles

function AccountMenu() {
    const [isOpen, setIsOpen] = useState(false);
    const menuRef = useRef(null);
    const navigate = useNavigate();

    const handleLogout = async () => {
        const token = localStorage.getItem('token')
        
        try {
            await fetchAPI_JSON('/api/auth/logout', {
                method: 'POST',
            });
        } catch (err) {
            console.error('Logout error:', err)
        } finally {
            // Remove from localStorage regardless
            localStorage.clear()
            navigate('/login')
        }
    };
    // Get user data
    const user = JSON.parse(localStorage.getItem('user'))

    // Close menu when clicking outside
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (menuRef.current && !menuRef.current.contains(event.target)) {
                setIsOpen(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    const toggleMenu = () => setIsOpen(!isOpen);

    const handleMenuItemClick = (action) => {
        setIsOpen(false);
        
        // Handle different actions
        switch(action) {
            case 'profile':
                // Navigate to profile
                break;
            case 'settings':
                // Navigate to settings
                break;
            case 'logout':
                // Handle logout
                handleLogout();
                break;
            default:
                break;
        }
    };

    // Generate initials for avatar
    const getInitials = (name) => {
        return name.split(' ').map(n => n[0]).join('').toUpperCase();
    };

    return (
        <div className="account-menu" ref={menuRef}>
            {/* Account Icon/Avatar */}
            <button 
                className={`account-button ${isOpen ? 'active' : ''}`}
                onClick={toggleMenu}
                aria-label="Account menu"
            >
 
                <div className="avatar-placeholder">
                    {getInitials(user.name)}
                </div>

                
                {/* Dropdown arrow */}
                <svg 
                    className={`dropdown-arrow ${isOpen ? 'rotated' : ''}`}
                    width="12" 
                    height="12" 
                    viewBox="0 0 12 12"
                >
                    <path d="M3 5l3 3 3-3" stroke="currentColor" strokeWidth="1.5" fill="none"/>
                </svg>
            </button>

            {/* Dropdown Menu */}
            {isOpen && (
                <div className="account-dropdown">
                    {/* User Info Section */}
                    <div className="user-info">
                        <div className="user-avatar">
                            {user.avatar ? (
                                <img src={user.avatar} alt="User avatar" />
                            ) : (
                                <div className="avatar-placeholder">
                                    {getInitials(user.name)}
                                </div>
                            )}
                        </div>
                        <div className="user-details">
                            <div className="user-name">{user.name}</div>
                            <div className="user-email">{user.email}</div>
                        </div>
                    </div>

                    <div className="menu-divider"></div>

                    {/* Menu Items */}
                    <div className="menu-items">

                        <button 
                            className="menu-item logout"
                            onClick={() => handleMenuItemClick('logout')}
                        >
                            <svg width="16" height="16" viewBox="0 0 16 16">
                                <path d="M3 3a2 2 0 012-2h3.5a2 2 0 012 2v1a.5.5 0 01-1 0V3a1 1 0 00-1-1H5a1 1 0 00-1 1v10a1 1 0 001 1h3.5a1 1 0 001-1v-1a.5.5 0 011 0v1a2 2 0 01-2 2H5a2 2 0 01-2-2V3z" fill="currentColor"/>
                                <path d="M7.5 8a.5.5 0 01.5-.5h5.793l-2.147-2.146a.5.5 0 01.708-.708l3 3a.5.5 0 010 .708l-3 3a.5.5 0 01-.708-.708L13.293 8.5H8a.5.5 0 01-.5-.5z" fill="currentColor"/>
                            </svg>
                            Sign Out
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}

export default AccountMenu;