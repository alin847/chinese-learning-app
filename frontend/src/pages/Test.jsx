import { useParams } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Loading from '../components/Loading';
import Header from '../components/Header';
import TestStart from '../components/TestStart';
import TestQuestion from '../components/TestQuestion';
import TestAnswer from '../components/TestAnswer';
import TestEnd from '../components/TestEnd';
import ProgressBar from '../components/ProgressBar';

import "./Test.css";

function Test() {
    // Get the current URL path
    const params = useParams();
    const type = params.type;

    // State for tracking the state of the test
    const [start, setStart] = useState(true);
    const [end, setEnd] = useState(false);
    const [loading, setLoading] = useState(true);
    const [time, setTime] = useState(0); // Track time spent on each question
    const [timeStart, setTimeStart] = useState(false); // Track if the timer has started
    
    useEffect(() => {
        // Start the timer when the component mounts
        const timer = setInterval(() => {
            if (timeStart) {
                setTime(prevTime => prevTime + 1);
            }
        }, 1000); // Increment time every second
        return () => clearInterval(timer); // Cleanup the timer on unmount
    }, [timeStart]);


    // Fetch questions based on the type
    const [questions, setQuestions] = useState([]);
    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
    useEffect (() => {
        const loadQuestions = async () => {
            const fetchedQuestions = await fetchQuestions(type);
            setQuestions(fetchedQuestions);
            setLoading(false);
        }
        loadQuestions();
    }, [type]);

    
    // Track user's answer
    const [answerData, setAnswerData] = useState({});
    const [showAnswer, setShowAnswer] = useState(false);
    
    // Track wrong answers (simplified)
    const [wrongSimplified, setWrongSimplified] = useState([]);

    // Function to handle onClick of the start button
    const handleStart = () => {
        setStart(false);
        setTimeStart(true); // Start the timer
    }

    // Function to handle the next question
    const handleNext = () => {
        if (currentQuestionIndex < questions.length - 1) {
            setCurrentQuestionIndex(currentQuestionIndex + 1);
            setShowAnswer(false);
            setTimeStart(true); // Restart the timer for the next question
        } else {
            // Handle end of test logic here, e.g., show results or reset
            setShowAnswer(false);
            setEnd(true);
        }
    }

    // Function to handle the answer submission
    const handleAnswer = async (answer) => {
        setLoading(true);
        setTimeStart(false); // Stop the timer for this question
        const timeTaken = time; // Capture the time taken for this question
        setTime(0); // Reset time for the next question
        // update time spent for user data
        fetch('http://localhost:4000/api/progress/time_spent', {
            method: 'PUT',
            headers: {
                "Authorization": `Bearer ${localStorage.getItem('token')}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ time_spent: timeTaken })
        })
        .catch(err => {
            console.error('Error updating time spent:', err);
        });
        // update number of questions answered
        fetch('http://localhost:4000/api/progress/practice_completed', {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json'
            },
        })
        .catch(err => {
            console.error('Error updating questions answered:', err);
        }); 
        // Fetch answer data from the backend
        const answerResult = await fetchAnswerData(questions[currentQuestionIndex], answer);
        setAnswerData(answerResult);
        
        let score;
        if (answerResult.correct === false) {
            setWrongSimplified(prev => [...prev, questions[currentQuestionIndex].simplified]);
            score = 1;
        } else {
            score = timeToScore(questions[currentQuestionIndex].type, timeTaken);
        }
        
        updateVocab(questions[currentQuestionIndex].simplified_id, score);
        setShowAnswer(true);
        setLoading(false);
    };

    if (loading) {
        return <Loading />;
    }
    if (start) {
        return (
            <>
            <Header isLoggedIn={true} />
            <div className="test-page">
                <div className="test-container">
                    <TestStart type={type} onStart={handleStart} />
                </div>
            </div>
            </>
        );
    }
    if (end) {
        const score = (questions.length - wrongSimplified.length) / questions.length * 100;
        return (
            <>
            <Header isLoggedIn={true} />
            <div className="test-page">
                <div className="test-container">
                    <TestEnd wrongSimplified={wrongSimplified} score={score} />
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
                <ProgressBar currentIndex={currentQuestionIndex+1} length={questions.length}/>

                {!showAnswer ? (
                    <TestQuestion 
                        question={questions[currentQuestionIndex]}
                        onAnswer={handleAnswer}
                    />
                ) : (
                    <TestAnswer 
                        answerData={answerData}
                        onNext={handleNext}
                    />
                )}
            </div>

        </div>
        </>
    )
}

export default Test;

const fetchQuestions = async (type) => {
    try {
        const response = await fetch(`http://localhost:4000/api/practice/${type}`, {
            method: 'GET',
            headers: {
                "Authorization": `Bearer ${localStorage.getItem('token')}`,
                "Content-Type": "application/json"
            }
        });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        return data; // Data is an array of questions
    } catch (error) {
        console.error('Error fetching questions:', error);
        return [];
    }
};

const fetchAnswerData = async (question, answer) => {
    try {
        const response = await fetch(`http://localhost:4000/api/practice/check-answer`, {
            method: 'POST',
            headers: {
                "Authorization": `Bearer ${localStorage.getItem('token')}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question, answer })
        });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        return data; // Data contains the answer feedback
    } catch (error) {
        console.error('Error fetching answer data:', error);
        return null; // Return null or handle error as needed
    }
};



// SM-2 algorithm for spaced repetition
function SM2(score, repetitions, interval, easeFactor) {
    // score: 0-5, repetitions: int, interval: int, easeFactor: float
    if (score >= 3) { // Correct answer
        if (repetitions === 0) {
            interval = 1;
        } else if (repetitions === 1) {
            interval = 6;
        } else {
            interval = Math.round(interval * easeFactor);
        }
        repetitions += 1;
    } else { // Incorrect answer
        repetitions = 0;
        interval = 1;
    }

    easeFactor = Math.max(1.3, easeFactor + (0.1 - (5 - score) * (0.08 + (5 - score) * 0.02)));

    return { repetitions, interval, easeFactor };
};

function timeToScore(type, time) {
    switch (type) {
        case 'dictation-sentence':
            if (time < 20) {
                return 5; // Excellent
            }
            if (time < 40) {
                return 4; // Good
            }
            return 3; // Moderate
        case 'dictation-simplified':
            if (time < 10) {
                return 5; // Excellent
            }
            if (time < 20) {
                return 4; // Good
            }
            return 3; // Moderate
        case 'writing':
            if (time < 30) {
                return 5; // Excellent
            }
            if (time < 60) {
                return 4; // Good
            }
            return 3; // Moderate
        case 'speaking':
            if (time < 10) {
                return 5; // Excellent
            }
            if (time < 20) {
                return 4; // Good
            }
            return 3; // Moderate
    }
};


/* 
The `updateVocab` function updates the user's vocabulary bank based on their performance in the test.
It fetches the current vocab data for the given `simplified_id`, applies the SM-2 algorithm to calculate 
the new repetitions, interval, and ease factor, and then sends the updated vocab data back to the server.
*/
const updateVocab = async (simplified_id, score) => {
    // Fetch the vocab for the user from their vocab bank
    const response = await fetch(`http://localhost:4000/api/vocab?simplified_id=${simplified_id}`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json'
        }
    });
    if (!response.ok) {
        console.error('Failed to fetch vocab bank:', response.statusText);
        return;
    }
    const vocab = await response.json();

    // Update the vocab bank using the SM-2 algorithm
    const updatedVocab = SM2(score, vocab.repetitions, vocab.interval, vocab.ease_factor);
    await fetch(`http://localhost:4000/api/vocab`, {
        method: 'PUT',
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            simplified_id: simplified_id,
            repetitions: updatedVocab.repetitions,
            interval: updatedVocab.interval,
            ease_factor: updatedVocab.easeFactor
        })
    });
};
