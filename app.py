from flask import Flask, render_template, request, send_file
import yt_dlp
import uuid
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/baixar', methods=['POST'])
def baixar():
    url = request.form.get('url')
    if not url:
        return "URL inválida", 400

    video_id = str(uuid.uuid4())
    output_path = f"/tmp/{video_id}.mp4"  # /tmp é obrigatório no Railway free tier

    ydl_opts = {
        'format': 'best',
        'outtmpl': output_path
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return send_file(output_path, as_attachment=True)
    finally:
        if os.path.exists(output_path):
            os.remove(output_path)
