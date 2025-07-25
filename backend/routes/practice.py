from backend.models.vocab_bank import get_random_practice
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from google import genai
from google.genai import types
from google.cloud import texttospeech
from google.cloud import speech
import difflib
import json
import base64
import random

bp = Blueprint('practice', __name__, url_prefix='/api/practice')

@bp.route('/mixed', methods=['GET'])
@jwt_required()
def mixed():
    """
    Render the mixed practice page. Generates a mix of dictation sentences, dictation simplified,
    speaking, and writing questions. 4 dictation sentences, 3 dictation simplified, 2 writing, 
    and 1 speaking question.
    Question format:
    - Check the individual routes for the specific question formats.
    """
    user_id = get_jwt_identity()
    practice_words = get_random_practice(user_id, 10)
    simplified = [word['simplified'] for word in practice_words]

    # 4 dictation sentences, and 1 speaking question
    sentences = make_dictation_sentences(simplified[:5])
    questions = []

    # 4 dictation sentences
    for i in range(4):
        question = {
            'type': 'dictation-sentence',
            'simplified_id': practice_words[i]['simplified_id'],
            'simplified': practice_words[i]['simplified'],
            'sentence': sentences[i],
            'audio': base64.b64encode(tts(sentences[i])).decode('utf-8')
        }
        questions.append(question)

    # 1 speaking question
    for i in range(4,5):
        question = {
            'type': 'speaking',
            'simplified_id': practice_words[i]['simplified_id'],
            'simplified': practice_words[i]['simplified'],
            'sentence': sentences[i]
        }
        questions.append(question)

    # 3 dictation simplified questions
    for word in practice_words[5:8]:
        question = {
            'type': 'dictation-simplified',
            'simplified_id': word['simplified_id'],
            'simplified': word['simplified'],
            'definitions': word['definitions'],
            'audio': base64.b64encode(tts(word["simplified"])).decode('utf-8')
        }
        questions.append(question)

    # 2 writing questions
    for word in practice_words[8:10]:
        question = {
            'type': 'writing',
            'simplified_id': word['simplified_id'],
            'simplified': word['simplified']
        }
        questions.append(question)

    # Shuffle the questions to mix them up
    random.shuffle(questions)
    return jsonify(questions), 200

@bp.route('/dictation-sentence', methods=['GET'])
@jwt_required()
def dictation_sentence():

    """
    Render the dictation practice page. Generates random sentences for dictation practice.
    Question format:
    {
        'type': 'dictation-sentence',
        'simplified_id': 'simplified_id',
        'simplified': 'word in simplified Chinese',
        'sentence': 'Generated sentence using the word',
        'audio': 'Audio content of the sentence'
    }
    """
    user_id = get_jwt_identity()
    practice_words = get_random_practice(user_id, 10)
    simplified = [word['simplified'] for word in practice_words]
    sentences = make_dictation_sentences(simplified)
    questions = []
    for i, sentence in enumerate(sentences):
        question = {
            'type': 'dictation-sentence',
            'simplified_id': practice_words[i]['simplified_id'],
            'simplified': practice_words[i]['simplified'],
            'sentence': sentence,
            'audio': base64.b64encode(tts(sentence)).decode('utf-8')
        }
        questions.append(question)

    return jsonify(questions), 200
    

@bp.route('/dictation-simplified')
@jwt_required()
def dictation_simplified():
    """
    Render the dictation practice page for simplified Chinese words.
    Question format:
    {
        'type': 'dictation-simplified',
        'simplified_id': 'simplified_id',
        'simplified': 'word in simplified Chinese',
        'definitions': 'Definitions of the word',
        'audio': 'Audio content of the word'
    }
    """
    user_id = get_jwt_identity()
    practice_words = get_random_practice(user_id, 10)
    questions = []
    for word in practice_words:
        question = {
            'type': 'dictation-simplified',
            'simplified_id': word['simplified_id'],
            'simplified': word['simplified'],
            'definitions': word['definitions'],
            'audio': base64.b64encode(tts(word["simplified"])).decode('utf-8')
        }
        questions.append(question)

    return jsonify(questions), 200


@bp.route('/speaking')
@jwt_required()
def speaking():
    """Render the speaking practice page.
    Question format:
    {
        'type': 'speaking',
        'simplified_id': 'simplified_id',
        'simplified': 'word in simplified Chinese',
        'sentence': 'Generated sentence using the word',
    }
    """
    user_id = get_jwt_identity()
    practice_words = get_random_practice(user_id, 5)
    simplified = [word['simplified'] for word in practice_words]
    sentences = make_dictation_sentences(simplified)
    questions = []
    for i, sentence in enumerate(sentences):
        question = {
            'type': 'speaking',
            'simplified_id': practice_words[i]['simplified_id'],
            'simplified': practice_words[i]['simplified'],
            'sentence': sentence
        }
        questions.append(question)

    return jsonify(questions), 200


@bp.route('/writing')
@jwt_required()
def writing():
    """
    Render the writing practice page.
    Question format:
    {
        'type': 'writing',
        'simplified_id': 'simplified_id',
        'simplified': 'word in simplified Chinese'
    }
    """
    user_id = get_jwt_identity()
    practice_words = get_random_practice(user_id, 10)
    questions = []
    for word in practice_words:
        question = {
            'type': 'writing',
            'simplified_id': word['simplified_id'],
            'simplified': word['simplified']
        }
        questions.append(question)

    return jsonify(questions), 200
    

@bp.route('/check-answer', methods=['POST'])
@jwt_required()
def check_answer():
    """
    Checks the user's answer for a given question type.
    Expects JSON data with the question format and the user's answer.
    """
    KEY = {
        'dictation-sentence': check_dictation_sentence,
        'dictation-simplified': check_dictation_simplified,
        'speaking': check_speaking,
        'writing': check_writing
    }

    data = request.get_json()
    question = data.get('question')
    question_type = question['type']
    user_answer = data.get('answer')

    if not question_type or question_type not in KEY:
        return jsonify({'error': 'Invalid question type.'}), 400
    if not user_answer:
        return jsonify({'error': 'Missing answer or simplified_id.'}), 400
    
    result = KEY[question_type](question, user_answer)
    return jsonify(result), 200

# HELPER
def tts(text):
    """Text-to-Speech synthesis for the given text."""
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="cmn-CN",
        name="cmn-CN-Chirp3-HD-Achernar"
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=0.9,
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    return response.audio_content


def stt(audio_bytes):
    """
    Speech-to-Text transcription for the given audio bytes.
    Returns the transcribed text.
    """
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_bytes)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
        language_code="cmn-Hans-CN",
        enable_automatic_punctuation=True,
    )

    response = client.recognize(config=config, audio=audio)
    
    # Combine all results into a single transcript
    transcript = "".join([result.alternatives[0].transcript for result in response.results])
    
    return transcript


def make_dictation_sentences(simplified):
    """
    Generates dictation questions for the given list of simplified Chinese words. Returns
    a list of sentences in order.
    """
    text = f"""
            Please generate one random example chinese sentence for each of the following words: 
            {', '.join(simplified)}.
            Return the sentences in the following list format in order:
            [<sentence1>, <sentence2>, <sentence3>, ...]
            Do not include any other text.
            """
    
    client = genai.Client()
    for _ in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=text,
                config=types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(thinking_budget=0), # Disables thinking
                ),
            )
            result = json.loads(response.text)
            if isinstance(result, list) and len(result) == len(simplified):
                return result
        except Exception:
            continue

    return None


def check_dictation_sentence(question, user_answer):
    """
    Checks the user's answer for a dictation sentence question.
    Returns 
    {
        'type': 'dictation-sentence',
        'correct': bool, # True if the answer is correct, False otherwise
        'simplified': str, # The simplified word to be dictated
        'sentence': str, # The sentence to be dictated
        'answer': str, # The user's answer
        'sentence_indices': list of indices where the sentence are same as the user's answer,
        'answer_indices': list of indices where the user's answer are same as the sentence,
    }
    """
    # For dictation sentences, we check if the simplified word is in the user's answer
    # and if the sentence is close enough to the user's answer
    similarity = difflib.SequenceMatcher(None, question['sentence'], user_answer).ratio()
    if similarity > 0.7 and question['simplified'] in user_answer:
        correct = True
    else:
        correct = False
    
    # Find indices where the user's answer matches the correct answer
    expected_indices, got_indices = find_matching_indices(question['sentence'], user_answer)

    return {
        'type': 'dictation-sentence',
        'correct': correct,
        'simplified': question['simplified'],
        'sentence': question['sentence'],
        'answer': user_answer,
        'sentence_indices': expected_indices,
        'answer_indices': got_indices
    }


def check_dictation_simplified(question, user_answer):
    """
    Checks the user's answer for a dictation simplified question.
    Returns 
    {
        'type': 'dictation-simplified',
        'correct': bool, # True if the answer is correct, False otherwise
        'simplified': str, # The simplified word to be dictated
        'answer': str, # The user's answer
        'simplified_indices': list of indices where the simplified word matches the user's answer,
        'answer_indices': list of indices where the user's answer matches the simplified word,
    }
    """
    # For dictation simplified, we check if the user's answer matches the simplified word
    if question['simplified'] == user_answer:
        correct = True
    else:
        correct = False
    
    # Find indices where the user's answer matches the simplified word
    expected_indices, got_indices = find_matching_indices(question['simplified'], user_answer)

    return {
        'type': 'dictation-simplified',
        'correct': correct,
        'simplified': question['simplified'],
        'answer': user_answer,
        'simplified_indices': expected_indices,
        'answer_indices': got_indices
    }


def check_speaking(question, user_answer):
    """
    Checks the user's answer for a speaking question.
    Returns 
    {
        'type': 'speaking',
        'correct': bool, # True if the answer is correct, False otherwise
        'simplified': str, # The simplified word to be used in the sentence
        'sentence': str, # The sentence to be spoken
        'answer': str, # The user's answer
        'sentence_indices': list of indices where the sentence matches the user's answer,
        'answer_indices': list of indices where the user's answer matches the sentence,
    }
    """
    # user_answer is base64 audio
    audio_bytes = base64.b64decode(user_answer)

    transcript = stt(audio_bytes)

    # For speaking questions, we check if the sentence is close enough to the user's answer
    # and if the simplified word is in the user's answer
    similarity = difflib.SequenceMatcher(None, question['sentence'], transcript).ratio()
    if similarity > 0.7 and question['simplified'] in transcript:  # Adjust threshold as needed
        correct = True
    else:
        correct = False
    
    # Find indices where the user's answer matches the sentence
    expected_indices, got_indices = find_matching_indices(question['sentence'], transcript)
    

    return {
        'type': 'speaking',
        'correct': correct,
        'simplified': question['simplified'],
        'sentence': question['sentence'],
        'answer': transcript,
        'sentence_indices': expected_indices,
        'answer_indices': got_indices
    }


def check_writing(question, user_answer):
    """
    Checks the user's answer for a writing question.
    Returns
    {
        'type': 'writing',
        'correct': bool, # True if the answer is correct, False otherwise
        'simplified': str, # The simplified word to be used in the sentence
        'answer': str, # The user's answer
        'grammar_bool': bool, # True if the grammar is correct, False otherwise
        'grammar_comment': str, # Comment on the grammar
        'meaning_bool': bool, # True if the meaning is correct, False otherwise
        'meaning_comment': str, # Comment on the meaning
    }
    """
    text = f"""
            Strictly check the grammar of the provided sentence. Then check if it makes sense as is. Provide a short comment as if you were a teacher.
            Sentence: {user_answer}
            Format the answer in the following array format:
            [<grammar_bool>, <grammar_comment>, <meaning_bool>, <meaning_comment>]
            Do not include any other text.
            """
    client = genai.Client()
    for _ in range(3):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=text,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=0),  # Disables thinking
            ),
        )
        try:
            result = json.loads(response.text)
            break  # Exit loop if JSON is valid
        except json.JSONDecodeError:
            continue  # Retry if the response is not valid JSON
    
    grammar_bool, grammar_comment, meaning_bool, meaning_comment = result
    # check if user_answer contains the simplified word
    if question['simplified'] in user_answer and meaning_bool and grammar_bool:
        correct = True
    else:
        correct = False
    
    return {
        'type': 'writing',
        'correct': correct,
        'simplified': question['simplified'],
        'answer': user_answer,
        'grammar_bool': grammar_bool,
        'grammar_comment': grammar_comment,
        'meaning_bool': meaning_bool,
        'meaning_comment': meaning_comment
    }


def find_matching_indices(expected, got):

    """
    Finds the indices of where the expected and got strings match.
    Returns a tuple of two lists:
    - expected_indices: indices where the expected string matches the got string
    - got_indices: indices where the got string matches the expected string
    """
    matcher = difflib.SequenceMatcher(None, expected, got)
    expected_indices = []
    got_indices = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            expected_indices.extend(range(i1, i2))
            got_indices.extend(range(j1, j2))
    return expected_indices, got_indices



if __name__ == "__main__":
    # test check_writing
    question = {
        'type': 'writing',
        'simplified_id': '1',
        'simplified': '汉字'
    }
    user_answer = '我在写做业。'
    print(check_writing(question, user_answer))