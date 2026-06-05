#!/usr/bin/env python3
"""Local TTS server dùng edge-tts (giọng Neural Microsoft, miễn phí)"""

import asyncio, io
from flask import Flask, request, Response
import edge_tts

app = Flask(__name__)

VOICES = {
    "XiaoxiaoNeural": "zh-CN-XiaoxiaoNeural",
    "YunxiNeural":    "zh-CN-YunxiNeural",
    "XiaohanNeural":  "zh-CN-XiaohanNeural",
    "YunjianNeural":  "zh-CN-YunjianNeural",
    "XiaoyiNeural":   "zh-CN-XiaoyiNeural",
}

def add_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.route("/voices")
def voices():
    return add_cors(app.response_class(
        response=str(list(VOICES.keys())),
        mimetype="application/json"
    ))

@app.route("/tts")
def tts():
    text  = request.args.get("text", "你好")
    voice = VOICES.get(request.args.get("voice", "XiaoxiaoNeural"), "zh-CN-XiaoxiaoNeural")
    rate  = request.args.get("rate", "+0%")
    pitch = request.args.get("pitch", "+0Hz")

    audio = asyncio.run(_synthesize(text, voice, rate, pitch))

    resp = Response(audio, mimetype="audio/mpeg")
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp

async def _synthesize(text, voice, rate, pitch):
    buf = io.BytesIO()
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            buf.write(chunk["data"])
    return buf.getvalue()

if __name__ == "__main__":
    print("✅ TTS Server đang chạy tại http://localhost:5050")
    print("   Nhấn Ctrl+C để dừng.")
    app.run(host="localhost", port=5050, debug=False)
