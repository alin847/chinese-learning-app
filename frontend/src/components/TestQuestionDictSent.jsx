import { useState } from 'react';
import { GiSpeaker } from "react-icons/gi";
import './TestQuestionDictSent.css';

function TestQuestionDictSent({ question, onAnswer }) {
    const [userAnswer, setUserAnswer] = useState('');


    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!userAnswer.trim()) {
            return;
        }


        try {
            await onAnswer(userAnswer);
        } catch (error) {
            console.error('Error submitting answer:', error);
        }

    };

    return (
        <div className="test-question">
            <div className="question-content">
                <h2>Write down what you hear.</h2>
                
                <div
                    className="audio-icon"
                    onClick={() => {
                            const base64Audio = question.audio;
                            const audioSrc = "data:audio/mp3;base64," + base64Audio;
                            const audio = new Audio(audioSrc);
                            audio.play();
                    }}
                >
                    <GiSpeaker size={200} color="black"/>
                </div>
            </div>

            <form className="question-submission" onSubmit={handleSubmit}>
                <textarea
                    value={userAnswer}
                    onChange={(e) => setUserAnswer(e.target.value)}
                    placeholder="Type your answer here..."
                />
                <button type="submit">Submit Answer</button>
            </form>
        </div>
    );
}

export default TestQuestionDictSent;