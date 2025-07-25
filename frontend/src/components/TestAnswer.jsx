import TestAnswerDictSent from './TestAnswerDictSent';
import TestAnswerDictSimp from './TestAnswerDictSimp';
import TestAnswerWriting from './TestAnswerWriting';
import TestAnswerSpeaking
 from './TestAnswerSpeaking';
function TestAnswer( { answerData, onNext } ) {
    const mapping = {
        'dictation-sentence': (<TestAnswerDictSent answerData={answerData} onNext={onNext} />),
        'dictation-simplified': (<TestAnswerDictSimp answerData={answerData} onNext={onNext} />),
        'writing': (<TestAnswerWriting answerData={answerData} onNext={onNext} />),
        'speaking': (<TestAnswerSpeaking answerData={answerData} onNext={onNext} />)
    }

    return mapping[answerData.type]
}

export default TestAnswer;