from flask import Flask, request, send_file
import subprocess
import os

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert():
    if 'video' not in request.files:
        return "Video file is required", 400

    video_file = request.files['video']
    if video_file.filename == '':
        return "No selected file", 400

    video_path = os.path.join("/tmp", video_file.filename)
    audio_path = os.path.splitext(video_path)[0] + '.mp3'

    video_file.save(video_path)

    # Use FFmpeg to convert video to audio
    subprocess.run(['ffmpeg', '-i', video_path, '-vn', '-ab', '128k', '-ar', '44100', '-y', audio_path])

    return send_file(audio_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

