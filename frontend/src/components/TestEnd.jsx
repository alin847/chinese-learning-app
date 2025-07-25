import { useNavigate } from 'react-router-dom';
import '../pages/Test.css';

function TestEnd({ wrongSimplified, score }) {
    const navigate = useNavigate();

    return (
        <div className="test-end">
            <div className="test-end-content">
                <h1>Your score: {score}%</h1>

                {wrongSimplified.length === 0 ? (null) : (
                    <>
                        <h2>Characters needing more review:</h2>
                        <ul>
                            {wrongSimplified.map((char, index) => (
                                <li key={index}>{char}</li>
                            ))}
                        </ul>
                    </>
                )}
                
                <img src="https://placehold.co/150x150" alt="icon (some yay pic)" />
            </div>

            <button onClick={() => navigate("/home")}>Return to home</button>
        </div>
    );
}

export default TestEnd;