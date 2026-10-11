import requests
import base64
import os

app = Flask(__name__)
CORS(app)

client = genai.Client(api_key=os.environ["AQ.Ab8RN6LAlg6xjyLbz84vwSef2wj7R1hjvgRXGPvdyENTBCMArA"])
GEMINI_API_KEY = os.environ.get("AQ.Ab8RN6LAlg6xjyLbz84vwSef2wj7R1hjvgRXGPvdyENTBCMArA")
MURF_API_KEY = os.environ.get("ap2_8cb0d0e7-6103-4862-b44b-8eb78c2889db")

if not GEMINI_API_KEY:
    raise RuntimeError("Missing GEMINI_API_KEY environment variable")
if not MURF_API_KEY:
    raise RuntimeError("Missing MURF_API_KEY environment variable")

client = genai.Client(api_key=GEMINI_API_KEY)

PROMPTS = {
"Summary": """
       You are a professional tourist guide.
@@ -42,65 +52,83 @@
Respond ONLY in {language}.
   """
}


def generate_speech(text, voice_id, locale):
    temp_audio = tempfile.NamedTemporaryFile(
        suffix=".mp3",
        delete=False
    )
    temp_audio = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
url = "https://global.api.murf.ai/v1/speech/stream"
headers = {
        "api-key": "ap2_28076e4e-1f6e-4315-82db-e55e6117a47c",
        "api-key": MURF_API_KEY,
"Content-Type": "application/json"
}
data = {
    "voice_id": voice_id,
    "text": text,
    "locale": locale,
    "model": "FALCON",
    "format": "MP3",
    "sampleRate": 24000,
    "channelType": "MONO"
        "voice_id": voice_id,
        "text": text,
        "locale": locale,
        "model": "FALCON",
        "format": "MP3",
        "sampleRate": 24000,
        "channelType": "MONO"
}
    response = requests.post(
        url,
        headers=headers,
        json=data
    )
    response = requests.post(url, headers=headers, json=data, timeout=120)
if response.status_code == 200:
with open(temp_audio.name, "wb") as f:
for chunk in response.iter_content(chunk_size=1024):
if chunk:
f.write(chunk)
else:
        print(f"Error: {response.status_code}")
        print(f"Murf API error: {response.status_code} - {response.text}")
        raise RuntimeError(f"Murf voice generation failed: {response.status_code}")

return temp_audio


def generate_description(place, answer_type, language):
prompt = PROMPTS[answer_type].format(place=place, language=language)
response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        model="gemini-2.5-flash-lite",
contents=prompt
)
return response.text


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})


@app.route("/generate-audio-guide", methods=["POST"])
def generate_audio_guide():
    data = request.json
    place = data["place"]
    answer_type = data["answerType"]
    language = data["language"]
    voice_id = data["voiceId"]
    locale = data["locale"]
    text_description = generate_description(place, answer_type, language)
    audio_path = generate_speech(text_description, voice_id, locale)

    audio_bytes = open(audio_path.name, "rb").read()
    encoded_audio = base64.b64encode(audio_bytes).decode("utf-8")

    return {
        "description": text_description,
        "audioBase64": encoded_audio
    }
app.run(debug=True)
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON"}), 400

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400

    place = data.get("place")
    answer_type = data.get("answerType")
    language = data.get("language")
    voice_id = data.get("voiceId")
    locale = data.get("locale")

    if not all([place, answer_type, language, voice_id, locale]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        text_description = generate_description(place, answer_type, language)
        audio_path = generate_speech(text_description, voice_id, locale)
        with open(audio_path.name, "rb") as audio_file:
            audio_bytes = audio_file.read()
        encoded_audio = base64.b64encode(audio_bytes).decode("utf-8")
        return jsonify({
            "description": text_description,
            "audioBase64": encoded_audio
        })
    except Exception as exc:
        app.logger.exception("Audio guide generation failed")
        return jsonify({"error": str(exc)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)