import { FaTimes, FaCheck } from "react-icons/fa";
import './TestAnswerSpeaking.css';

function TestAnswerSpeaking({ answerData, onNext }) {
    const correct = answerData.correct;
    const simplified = answerData.simplified;
    const sentence = answerData.sentence;
    const answer = answerData.answer;
    const sentence_indices = answerData.sentence_indices;
    const answer_indices = answerData.answer_indices;

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
                <h3>Expected Answer: <ColorSentence sentence={sentence} greenIndices={sentence_indices} /></h3>
                <h3>Your Answer: <ColorSentence sentence={answer} greenIndices={answer_indices} /></h3>
            </div>

            <button onClick={onNext}>Next</button>
        </div>
    );
}

function ColorSentence({ sentence, greenIndices }) {
  return (
    <span>
      {sentence.split('').map((char, index) => {
        const isGreen = greenIndices.includes(index);
        const color = isGreen ? 'green' : 'red';
        return (
          <span key={index} style={{ color }}>
            {char}
          </span>
        );
      })}
    </span>
  );
}


export default TestAnswerSpeaking