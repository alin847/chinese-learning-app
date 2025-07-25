import "../pages/Test";
import TestQuestionDictSent from "./TestQuestionDictSent";
import TestQuestionDictSimp from "./TestQuestionDictSimp";
import TestQuestionWriting from "./TestQuestionWriting";
import TestQuestionSpeaking from "./TestQuestionSpeaking";

function TestQuestion( { question, onAnswer } ) {
    const mapping = {
        'dictation-sentence': (<TestQuestionDictSent question={question} onAnswer={onAnswer} />),
        'dictation-simplified': (<TestQuestionDictSimp question={question} onAnswer={onAnswer} />),
        'writing': (<TestQuestionWriting question={question} onAnswer={onAnswer} />),
        'speaking': (<TestQuestionSpeaking question={question} onAnswer={onAnswer} />),
    }

    return mapping[question.type]
}

export default TestQuestion;

