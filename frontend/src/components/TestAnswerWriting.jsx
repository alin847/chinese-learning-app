import { FaTimes, FaCheck } from "react-icons/fa";
import './TestAnswerWriting.css';

function TestAnswerDictSent({ answerData, onNext }) {
    const correct = answerData.correct;
    const simplified = answerData.simplified;
    const answer = answerData.answer;
    const grammar_bool = answerData.grammar_bool;
    const grammar_comment = answerData.grammar_comment;
    const meaning_bool = answerData.meaning_bool;
    const meaning_comment = answerData.meaning_comment;

    return (
        <div className="test-answer">
            <div className="test-answer-header">
                <h2>Vocabulary Tested: {simplified}</h2>
                {correct ? (
                    <FaCheck size={150} color="green" />
                ) : (
                    <FaTimes size={150} color="red" />
                )}
            </div>

            <div className="test-answer-comment">
                <h3>Your Answer: {answer}</h3>
                <h4 style={{ color: grammar_bool ? 'green' : 'red' }}>
                    Grammar check: {grammar_comment}
                </h4>
                <h4 style={{ color: meaning_bool ? 'green' : 'red' }}>
                    Context check: {meaning_comment}
                </h4>
            </div>

            <button onClick={onNext}>Next</button>
        </div>
    );
}


export default TestAnswerDictSent;