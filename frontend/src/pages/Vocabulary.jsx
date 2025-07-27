
import HeaderHome from "../components/HeaderHome";
import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import SmallCards from "../components/SmallCards";
import Loading from "../components/Loading";
import HomeSidebar from "../components/HomeSidebar";
import { fetchAPI_JSON } from "../utils/api.jsx";

function Vocabulary() {
    const navigate = useNavigate();
    const [learningWords, setLearningWords] = useState([]);
    const [reviewingWords, setReviewingWords] = useState([]);
    const [masteredWords, setMasteredWords] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchVocabulary = async () => {
            try {
                const data = await fetchAPI_JSON('/api/vocab/all', { method: 'GET' });
                setLearningWords(data.learning_vocab);
                setReviewingWords(data.reviewing_vocab);
                setMasteredWords(data.mastered_vocab);
                setLoading(false);
            } catch (error) {
                console.error('Error fetching vocabulary:', error);
            };
        };
        fetchVocabulary();
    }, []);


    if (loading) {
        return <Loading />
    }
    
    return (
        <div className="vocabulary">
        <HeaderHome />
        
        <div className="home-container">
            <HomeSidebar activePage="vocabulary" />

            <main className="content">
            <h1>Vocabulary Bank</h1>
            
            <div className="subcontent">
                <h2>Add Words</h2>
                <div className="horizontal-line"></div>
                <div className="cards">
                    <div className="card" onClick={() => navigate('/search/recommended')}>
                        <img src="/lightbulb.png"/>
                        <h3>discover new words</h3>
                    </div>
                    <div className="card" onClick={() => navigate('/search')}>
                        <img src="/add.png" />
                        <h3>add words manually</h3>
                    </div>
                </div>
            </div>
            
            <div className="subcontent">
                <h2>Learning</h2>
                <div className="horizontal-line"></div>
                { learningWords.length === 0 ? (
                <p>No words currently in learning state.</p>
                ) : (
                <SmallCards items={learningWords} />
                )}
            </div>

            <div className="subcontent">
                <h2>Reviewing</h2>
                <div className="horizontal-line"></div>
                { reviewingWords.length === 0 ? (
                    <p>No words currently in reviewing state.</p>
                ) : (
                <SmallCards items={reviewingWords} />
                )}
            </div>

            <div className="subcontent">
                <h2>Mastered</h2>
                <div className="horizontal-line"></div>
                { masteredWords.length === 0 ? (
                    <p>No words currently in mastered state.</p>
                ) : (
                <SmallCards items={masteredWords} />
                )}
            </div>

            </main>

        </div>
        </div>
    )
};

export default Vocabulary;