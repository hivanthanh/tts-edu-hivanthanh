import asyncio, io, os
from flask import Flask, request, Response
from flask_cors import CORS
import edge_tts

app = Flask(__name__)
CORS(app)

VOICES = {
    "XiaoxiaoNeural": "zh-CN-XiaoxiaoNeural",
    "YunxiNeural":    "zh-CN-YunxiNeural",
    "XiaohanNeural":  "zh-CN-XiaohanNeural",
    "YunjianNeural":  "zh-CN-YunjianNeural",
    "XiaoyiNeural":   "zh-CN-XiaoyiNeural",
}

@app.route("/")
def index():
    return "TTS Server OK"

@app.route("/voices")
def voices():
    return {"voices": list(VOICES.keys())}

@app.route("/tts")
def tts():
    text  = request.args.get("text", "你好")
    voice = VOICES.get(request.args.get("voice", "XiaoxiaoNeural"), "zh-CN-XiaoxiaoNeural")
    rate  = request.args.get("rate", "+0%")
    pitch = request.args.get("pitch", "+0Hz")
    audio = asyncio.run(_synthesize(text, voice, rate, pitch))
    return Response(audio, mimetype="audio/mpeg")

async def _synthesize(text, voice, rate, pitch):
    buf = io.BytesIO()
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            buf.write(chunk["data"])
    return buf.getvalue()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port)
