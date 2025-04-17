from flask import Flask, request, send_file, jsonify
import os
from utils import detect_chart_type, image_to_video, matplotlib_to_video, add_voice_over, combine_video_audio
import matplotlib.pyplot as plt
import pickle
from io import BytesIO #denemeSatiri

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/upload-file', methods=['POST'])
def upload_file():
    """Kullanıcıdan dosya (PNG/JPG) alıp sesli video döndürür."""
    if 'image' not in request.files:
        return jsonify({"error": "Görüntü dosyası eksik!"}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "Dosya seçilmedi!"}), 400
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        return jsonify({"error": "Sadece PNG veya JPG dosyaları destekleniyor!"}), 400

    frame_rate = int(request.form.get('frame_rate', 30))
    duration = int(request.form.get('duration', 5))
    codec = request.form.get('codec', 'mp4v')

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        chart_type = detect_chart_type(file_path)
        video_path = os.path.join(OUTPUT_FOLDER, 'temp_video.mp4')
        final_path = os.path.join(OUTPUT_FOLDER, f'final_{file.filename}.mp4')

        temp_video = image_to_video(file_path, video_path, frame_rate, duration, codec)
        narration = f"This video shows a {chart_type}"
        audio_path = os.path.join(OUTPUT_FOLDER, 'voice_over.mp3')
        add_voice_over(narration, audio_path)
        combine_video_audio(temp_video, audio_path, final_path)

        os.remove(file_path)
        os.remove(temp_video)
        os.remove(audio_path)

        return send_file(final_path, mimetype='video/mp4', as_attachment=True)
    except Exception as e:
        return jsonify({"error": f"İşlem hatası: {str(e)}"}), 500

@app.route('/upload-object', methods=['POST'])
def upload_object():
    """Kullanıcıdan Matplotlib nesnesi alıp sesli video döndürür."""
    if 'object' not in request.files:
        return jsonify({"error": "Matplotlib nesnesi eksik!"}), 400
    file = request.files['object']
    if file.filename == '':
        return jsonify({"error": "Nesne seçilmedi!"}), 400

    frame_rate = int(request.form.get('frame_rate', 30))
    duration = int(request.form.get('duration', 5))
    codec = request.form.get('codec', 'mp4v')

    try:
        fig_data = pickle.load(file)
        if not isinstance(fig_data, plt.Figure):
            return jsonify({"error": "Geçersiz Matplotlib nesnesi!"}), 400

        temp_image = os.path.join(UPLOAD_FOLDER, 'temp.png')
        fig_data.savefig(temp_image, format='png')
        chart_type = detect_chart_type(temp_image)

        video_path = os.path.join(OUTPUT_FOLDER, 'temp_video.mp4')
        final_path = os.path.join(OUTPUT_FOLDER, 'final_object.mp4')
        temp_video = matplotlib_to_video(fig_data, video_path, frame_rate, duration, codec)

        narration = f"This video shows a {chart_type}"
        audio_path = os.path.join(OUTPUT_FOLDER, 'voice_over.mp3')
        add_voice_over(narration, audio_path)
        combine_video_audio(temp_video, audio_path, final_path)

        os.remove(temp_image)
        os.remove(temp_video)
        os.remove(audio_path)

        return send_file(final_path, mimetype='video/mp4', as_attachment=True)
    except Exception as e:
        return jsonify({"error": f"İşlem hatası: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)