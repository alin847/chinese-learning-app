import "../pages/Test.css"
// Change place holder image in final version
function TestStart({ type, onStart }) {
    return (
        <div className="test-start">
            <h1>Welcome to {mapping[type]} Practice</h1>
            <img src={`https://placehold.co/150x150`} alt={`icon`} />
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

