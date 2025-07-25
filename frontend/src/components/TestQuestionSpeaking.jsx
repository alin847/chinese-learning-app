import { useState, useRef } from 'react';
import './TestQuestionSpeaking.css';
import { FaPlayCircle, FaPauseCircle, FaCheckCircle, FaTimesCircle } from 'react-icons/fa';
import { CiMicrophoneOn } from "react-icons/ci";

function TestQuestionDictSent({ question, onAnswer }) {
    const [isRecording, setIsRecording] = useState(false);
    const [audioBlob, setAudioBlob] = useState(null);
    const mediaRecorderRef = useRef(null);
    const audioChunksRef = useRef([]);

    const startRecording = async () => {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorderRef.current = new MediaRecorder(stream);

        audioChunksRef.current = [];

        mediaRecorderRef.current.ondataavailable = event => {
            audioChunksRef.current.push(event.data);
        };

        mediaRecorderRef.current.onstop = () => {
            const blob = new Blob(audioChunksRef.current, { type: "audio/wav" });
            setAudioBlob(blob);
        };

        mediaRecorderRef.current.start();
        setIsRecording(true);
    };

    const stopRecording = () => {
        mediaRecorderRef.current.stop();
        setIsRecording(false);
    };

    const resetRecording = () => {
        setAudioBlob(null);
        audioChunksRef.current = [];
    };

    const handleClick = async () => {
        try {
            const base64Audio = await blobToBase64(audioBlob);
            onAnswer(base64Audio);
        } catch (error) {
            console.error('Error submitting answer:', error);
        }
    };

    return (
        <div className="test-question">
            <div className="question-content">
                <h2>Read the following sentence: {question.sentence}</h2>
            </div>

            <div className="question-submission">
                <div className={`microphone-icon${isRecording ? ' active' : ''}`}>
                    <CiMicrophoneOn size={200}/>
                </div>

                <div className="microphone-controls">
                    {audioBlob && 
                    <FaTimesCircle className="icon" onClick={() => resetRecording()} />
                    }

                    {!audioBlob && !isRecording &&
                    <FaPlayCircle className="icon" onClick={() => startRecording()} />
                    }

                    {!audioBlob && isRecording &&
                    <FaPauseCircle className="icon" onClick={() => stopRecording()} />
                    }

                    {audioBlob &&
                    <FaCheckCircle className="icon" onClick={() => handleClick()} />
                    }

                </div>
            </div>
        </div>
    );
}

function blobToBase64(blob) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      const base64data = reader.result.split(',')[1]; // Extract just the base64 part
      resolve(base64data); // This is the Base64 string (no prefix)
    };
    reader.onerror = reject;
    reader.readAsDataURL(blob); // Starts reading the blob
  });
}



export default TestQuestionDictSent;