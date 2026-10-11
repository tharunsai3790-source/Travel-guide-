// --- Constants ---
const VOICES = {
English: { Male: "Matthew", Female: "Alicia" },
Hindi: { Male: "Aman", Female: "Namrita" },
Tamil: { Male: "Murali", Female: "Iniya" },
Telugu: { Male: "Zion", Female: "Josie" }
};

const LOCALES = {
English: "en-US",
Hindi: "hi-IN",
Tamil: "ta-IN",
Telugu: "te-IN"
};

// Use a deploy-safe API URL.
// For local development, it will hit localhost.
// For Render deployment, replace the default value with your deployed backend URL.
const API_BASE_URL =
  window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://127.0.0.1:5000'
    : 'https://your-render-backend-url.onrender.com';

const GENERATE_AUDIO_GUIDE_API_URL = `${API_BASE_URL}/generate-audio-guide`;

// --- State ---
const state = {
@@ -122,59 +131,55 @@
});
});


// Generate Audio guide button Logic

const GENERATE_AUDIO_GUIDE_API_URL = "http://127.0.0.1:5000/generate-audio-guide";

generateButton.addEventListener('click', async () => {
generateButton.disabled = true;
generateButton.textContent = '⏳ Generating Audio...';

try {
const selectedLanguage = languageSelect.value;
const selectedVoice = state.voice;

const response = await fetch(GENERATE_AUDIO_GUIDE_API_URL, {
method: 'POST',
headers: { 'Content-Type': 'application/json' },
body: JSON.stringify({
place: state.place,
answerType: state.length,
language: selectedLanguage,
voiceId: VOICES[selectedLanguage][selectedVoice],
locale: LOCALES[selectedLanguage]
})
});

if (!response.ok) throw new Error('Generation failed');

const data = await response.json();

// Update UI with Result
transcriptText.textContent = data.description;
audioSection.classList.remove('hidden');

if (data.audioBase64) {
audioPlayer.src = `data:audio/mp3;base64,${data.audioBase64}`;
audioPlayer.load();
audioPlayer.classList.remove('hidden');
generateButton.textContent = 'Listen to Audio';
} else {
audioPlayer.classList.add('hidden');
generateButton.textContent = 'Audio Not Available';
}

} catch (err) {
console.error(err);
alert('Generation failed. Please check your connection.');
generateButton.textContent = 'Generate Audio Guide';
generateButton.disabled = false;
}
});

// Transcript Toggle
transcriptToggle.addEventListener('click', () => {
transcriptContent.classList.toggle('hidden');
transcriptArrow.classList.toggle('rotate-180');
});