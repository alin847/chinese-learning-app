from flask import Blueprint, request, jsonify, Response
from google.cloud import texttospeech
from src import tts_client

bp = Blueprint('tts', __name__, url_prefix='/api')

@bp.route('/tts', methods=['POST'])
def tts():
    """Text-to-Speech endpoint that synthesizes speech from text input."""
    data = request.get_json()
    text = data.get('text', '')
    if not text:
        return jsonify({'error': 'No text provided for synthesis.'}), 400
    try: 
        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Build the voice request
        voice = texttospeech.VoiceSelectionParams(
            language_code="cmn-CN",  # or "en-US" for English
            name="cmn-CN-Chirp3-HD-Achernar"
        )

        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        # Perform the text-to-speech request
        response = tts_client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )

        return Response(response.audio_content, mimetype='audio/mpeg')
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500