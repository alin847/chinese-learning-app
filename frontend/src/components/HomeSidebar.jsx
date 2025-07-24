import './HomeSidebar.css';

function HomeSidebar({ activePage }) {
    return (
        <nav className="sidebar">
                <h2>Home</h2>
                <div className="horizontal-line"></div>

                <a
                    href="/home"
                    className={`nav-bubble${activePage === 'dashboard' ? ' active' : ''}`}
                >
                    Dashboard
                </a>
                <a
                    href="/practice"
                    className={`nav-bubble${activePage === 'practice' ? ' active' : ''}`}
                >
                    Practice
                </a>
                <a
                    href="/vocabulary"
                    className={`nav-bubble${activePage === 'vocabulary' ? ' active' : ''}`}
                >
                    Vocabulary Bank
                </a>
                <a
                    href="/progress"
                    className={`nav-bubble${activePage === 'progress' ? ' active' : ''}`}
                >
                    Progress
                </a>
        </nav>
    );
}

export default HomeSidebar;