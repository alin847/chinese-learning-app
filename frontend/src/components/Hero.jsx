import { useNavigate } from 'react-router-dom';
import './Hero.css';

function Hero() {
    const navigate = useNavigate();
    return (
        <section className="hero">
            <div className="hero-content">
                <h1>The simple and effective way to master Chinese &mdash; totally free and no ads!</h1>
                <p>Ready for unlimited dictation, writing, and speaking exercises for free?</p>
                <button className="button-lg" onClick={() => navigate('/register')}>Get Started</button>
            </div>
        </section>
    )
}

export default Hero;