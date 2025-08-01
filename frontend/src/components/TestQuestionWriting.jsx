import { useState } from 'react';
import { PiPencilLineThin } from "react-icons/pi";
import './TestQuestionWriting.css';

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
                <h2>Write a sentence using: {question.simplified}</h2>
                
                <PiPencilLineThin size={200}/>
            </div>

            <form className="question-submission" onSubmit={handleSubmit}>
                <textarea
                    value={userAnswer}
                    onChange={(e) => setUserAnswer(e.target.value)}
                    placeholder="Type your answer here..."
                />
                <button type="submit">
                    Submit Answer
                </button>
            </form>
        </div>
    );
}

function PencilSVG() {
    return (
        <svg
            version="1.0"
            id="Layer_1"
            xmlns="http://www.w3.org/2000/svg"
            xmlnsXlink="http://www.w3.org/1999/xlink"
            viewBox="0 0 64 64"
            enableBackground="new 0 0 64 64"
            xmlSpace="preserve"
            width="150px"
            height="150px"
            fill="#000000"
        >
            <g id="SVGRepo_bgCarrier" strokeWidth="0"></g>
            <g id="SVGRepo_tracerCarrier" strokeLinecap="round" strokeLinejoin="round"></g>
            <g id="SVGRepo_iconCarrier">
                <path
                    fill="#231F20"
                    d="M62.828,12.482L51.514,1.168c-1.562-1.562-4.093-1.562-5.657,0.001c0,0-44.646,44.646-45.255,45.255
                    C-0.006,47.031,0,47.996,0,47.996l0.001,13.999c0,1.105,0.896,2,1.999,2.001h4.99c0.003,0,9.01,0,9.01,0s0.963,0.008,1.572-0.602
                    s45.256-45.257,45.256-45.257C64.392,16.575,64.392,14.046,62.828,12.482z M37.356,12.497l3.535,3.536L6.95,49.976l-3.536-3.536
                    L37.356,12.497z M8.364,51.39l33.941-33.942l4.243,4.243L12.606,55.632L8.364,51.39z M3.001,61.995c-0.553,0-1.001-0.446-1-0.999
                    v-1.583l2.582,2.582H3.001z M7.411,61.996l-5.41-5.41l0.001-8.73l14.141,14.141H7.411z M17.557,60.582l-3.536-3.536l33.942-33.94
                    l3.535,3.535L17.557,60.582z M52.912,25.227L38.771,11.083l2.828-2.828l14.143,14.143L52.912,25.227z M61.414,16.725l-4.259,4.259
                    L43.013,6.841l4.258-4.257c0.782-0.782,2.049-0.782,2.829-0.002l11.314,11.314C62.195,14.678,62.194,15.943,61.414,16.725z"
                ></path>
            </g>
        </svg>
    );
}

export default TestQuestionDictSent;