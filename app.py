import os
from flask import Flask, render_template, request, jsonify
from anthropic import Anthropic

app = Flask(__name__)
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/docs")
def docs():
    return render_template("landing.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    topic = data.get("topic", "")
    genre = data.get("genre", "pop")
    mood = data.get("mood", "upbeat")
    structure = data.get("structure", "verse-chorus-verse-chorus-bridge-chorus")

    prompt = f"""You are a Grammy-winning songwriter and lyricist. Write original song lyrics based on the user's input.

Topic/Theme: {topic}
Genre: {genre}
Mood: {mood}
Song structure: {structure}

Write complete, original lyrics in this format:

TITLE:
[A catchy, memorable song title]

LYRICS:
[Full lyrics with clear section labels like [Verse 1], [Chorus], [Bridge], etc.]
[Include natural rhythm and rhyme patterns appropriate for the genre]
[Make lyrics emotionally resonant and singable]

SONGWRITING NOTES:
- Tempo suggestion: [BPM range]
- Key suggestion: [Musical key that fits the mood]
- Vocal style: [How this should be sung]
- Production notes: [2-3 instrument/production suggestions]

RHYME SCHEME:
[Label the rhyme pattern used, e.g., ABAB, AABB]

Important:
- Lyrics must be 100% original
- Match the genre conventions (verse length, chorus repetition, etc.)
- Include vivid imagery and emotional hooks
- Make the chorus memorable and singable
- Avoid cliches — find fresh ways to express the theme"""

    try:
        message = client.messages.create(
            model="claude-3-5-haiku-latest",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        return jsonify({"result": message.content[0].text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5040)
