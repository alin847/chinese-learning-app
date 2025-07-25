import "../pages/Test.css"
// Change place holder image in final version
function TestStart({ type, onStart }) {
    return (
        <div className="test-start">
            <h1>Welcome to {mapping[type]} Practice</h1>
            <img src={imgMapping[type]} alt={`icon`} />
            <button 
                className="button-start" 
                onClick={onStart}
            >
                Start Practice
            </button>
        </div>
    );
}

export default TestStart;

const mapping = {
    "dictation-sentence": "Sentence Dictation",
    "dictation-simplified": "Character Dictation",
    "speaking": "Speaking",
    "writing": "Writing",
    "mixed": "Mixed",
}

const imgMapping = {
    "dictation-sentence": "/sentdict.png",
    "dictation-simplified": "/chardict.png",
    "speaking": "/speaking.png",
    "writing": "/writing.png",
    "mixed": "/mixed.png",
}
