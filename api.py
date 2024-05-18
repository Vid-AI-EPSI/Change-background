from flask import Flask, request, jsonify
import os
from BackgroundChangerAPI import BackgroundChanger

app = Flask(__name__)

@app.route('/change_bg', methods=['POST'])
def change_bg():
    video_file = request.files.get('video')
    if not video_file:
        return jsonify({'error': 'No video file provided'}), 400

    video_path = f"/tmp/{video_file.filename}"
    video_file.save(video_path)

    prompt = request.form.get('prompt')
    bg_file = request.files.get('background')

    if not prompt and not bg_file:
        return jsonify({'error': 'Either a prompt or a background file must be provided'}), 400

    bg_changer = BackgroundChanger(video_path)

    try:
        if bg_file:
            bg_path = f"/tmp/{bg_file.filename}"
            bg_file.save(bg_path)
            bg_changer.set_background_path(bg_path)
        elif prompt:
            bg_changer.set_background_prompt(prompt)
        
        bg_changer.change_bg()

        output_path = video_path.replace(".mp4", "__final.mp4")
        return jsonify({'message': 'Background changed successfully', 'output_path': output_path})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
