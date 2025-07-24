import { Link } from 'react-router-dom'
import { useEffect } from 'react';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

/**
 * HeaderHero component renders the header for the hero page, intended for logged-out users.
 * It displays a logo and a button that changes between "Sign In" and "Get Started" based on scroll position.
 * No props are required.
 */
function HeaderHero() {
    const [buttonText, setButtonText] = useState('Sign In');
    const [buttonTo, setButtonTo] = useState('/login');
    const navigate = useNavigate();

    useEffect(() => {
        function handleScroll() {
            const hero = document.querySelector('.hero');
            if (!hero) return;
            const heroBottom = hero.offsetTop + hero.offsetHeight;

            if (window.scrollY > heroBottom - 50) {
                setButtonText('Get Started');
                setButtonTo('/register');
            } else {
                setButtonText('Sign In');
                setButtonTo('/login');
            }
        }

        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

return (
    <header>
        <Link to={"/"} className="logo">
            <img src="/logo.jpg" alt="Logo" />
        </Link>

        <button onClick={() => navigate(buttonTo)}>{buttonText}</button>
    </header>
)
}

export default HeaderHero;
