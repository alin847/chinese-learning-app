import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import ProgressBar from '../components/ProgressBar';
import { fetchAPI_JSON } from '../utils/api';
import "./Test.css";
import "./Placement.css";

function Placement() {
    const [level, setLevel] = useState(3);
    const [question, setQuestion] = useState(null);
    const [excludedQuestionIds, setExcludedQuestionIds] = useState([]);
    const [count, setCount] = useState(0);
    const [correctAnswers, setCorrectAnswers] = useState([]);
    const [start, setStart] = useState(true);
    const [end, setEnd] = useState(false);
    
    const handleStart = async () => {
        try {
            const data = await fetchQuestion({ level: 3, excluded: [] });
            setQuestion(data);
            setStart(false);
        } catch (error) {
            console.error('Error fetching question:', error);
        }
    }

    const handleNext = async (answer) => {
        if (answer === question.answer) {
            setCorrectAnswers([...correctAnswers, level]);
            setLevel(Math.min(level + 1, 6));
        } else {
            setLevel(Math.max(level - 1, 1));
        }
        
        setExcludedQuestionIds([...excludedQuestionIds, question.question_id]);
        if (count + 1 >= 20) {
            setEnd(true);
            return;
        }
        setCount(count + 1);
        // Fetch the next question
        const data = await fetchQuestion({ level, excluded: excludedQuestionIds })
        setQuestion(data);
    }

    if (start) {
        return (
            <>
            <Header isLoggedIn={true} />
            <div className="test-page">
                <div className="test-container">
                    <PlacementStart onStart={handleStart} />
                </div>
            </div>
            </>
        );
    }

    if (end) {
        let hskLevel = 1;
        if (correctAnswers.length > 0) {
            hskLevel = Math.round(correctAnswers.reduce((sum, val) => sum + val, 0) / correctAnswers.length);
        }
        addInitialVocab(hskLevel)
            .then(() => {
                console.log('Initial vocabulary added successfully');
            })
            .catch(error => {
                console.error('Error adding initial vocabulary:', error);
            });

        return (
            <>
            <Header isLoggedIn={true} />
            <div className="test-page">
                <div className="test-container">
                    <PlacementEnd hskLevel={hskLevel} />
                </div>
            </div>
            </>
        );
    }

    return (
        <>
        <Header isLoggedIn={true} />
        <div className="test-page">
            <div className="test-container">
                <ProgressBar currentIndex={count+1} length={20}/>

                <PlacementQuestion
                    question={question}
                    onAnswer={handleNext}
                />
           
            </div>

        </div>
        </>
    )
}

async function fetchQuestion({ level, excluded }) {
    const data = await fetchAPI_JSON(`/api/placement/question`, {
        method: 'POST',
        body: JSON.stringify({ level, excluded }),
    });
    return data;
}

async function addInitialVocab(hskLevel) {
    await fetchAPI_JSON(`/api/placement/add-initial-vocab`, {
        method: 'POST',
        body: JSON.stringify({ level: hskLevel }),
    });
}

function PlacementStart({ onStart }) {
    return (
        <div className="placement-start">
            <h1>Welcome to the Placement Test</h1>
            <img src={`/testbubble.png`} alt={`icon`} />
            <button onClick={onStart}>Start Test</button>
        </div>
    );
}

function PlacementEnd({ hskLevel }) {
    const navigate = useNavigate();
    return (
        <div className="placement-end">
            <h1>Your estimated HSK Level is: {hskLevel}</h1>
            <p>Initial vocabulary has been added to your bank.</p>
            <img src={`/welldone.png`} alt={`icon`} />
            <button onClick={() => navigate("/home")}>Return to home</button>
        </div>
    );
}

function PlacementQuestion({ question, onAnswer }) {
    return (
        <div className="placement-question">
            <div className="question-content">
                <h2>{question.text}</h2>
            </div>
            
            <div className="question-submission">
                {question.options.map((option, index) => (
                    <button key={index} onClick={() => onAnswer(option)}>
                        {option}
                    </button>
                ))}

                <button key={4} onClick={() => onAnswer("")}>
                    I don't know
                </button>
            </div>
        </div>
    );
}

export default Placement;