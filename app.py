from flask import Flask, request, send_file, jsonify
import os
from utils import (
    detect_chart_type, 
    image_to_video, 
    matplotlib_to_video, 
    add_voice_over, 
    combine_video_audio,
    add_image_to_video,
    add_matplotlib_to_video,
    combine_videos,
    insert_image_into_video,
    insert_matplotlib_into_video
)
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import pickle
from io import BytesIO #trial

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/test')
def test():
    return "The test is working!"

@app.route('/upload-file', methods=['POST'])
def upload_file():
    """Take the file (PNG/JPG) from the user and return voice video."""
    if 'image' not in request.files:
        return jsonify({"error": "The image file is missing!"}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "The file was not selected!"}), 400
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        return jsonify({"error": "Only PNG or JPG files are supported!"}), 400

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
        return jsonify({"error": f"Transaction error: {str(e)}"}), 500

@app.route('/upload-object', methods=['POST'])
def upload_object():
    """Matplotlib object from the user takes the voice and returns voice video."""
    print("upload-object endpoint'i çağrıldı")
    
    if 'object' not in request.files:
        print("Hata: Matplotlib nesnesi eksik")
        return jsonify({"error": "Matplotlib nesnesi eksik!"}), 400
    file = request.files['object']
    if file.filename == '':
        print("Hata: Dosya seçilmedi")
        return jsonify({"error": "Nesne seçilmedi!"}), 400

    frame_rate = int(request.form.get('frame_rate', 30))
    duration = int(request.form.get('duration', 5))
    codec = request.form.get('codec', 'mp4v')
    print(f"Parameters received: frame_rate={frame_rate}, duration={duration}, codec={codec}")

    try:
        print("Matplotlib object is loaded ...")
        fig_data = pickle.load(file)
        if not isinstance(fig_data, plt.Figure):
            print("Error: invalid Matplotlib object")
            return jsonify({"error": "Invalid matplotlib object!"}), 400

        print("Temporary PNG is created...")
        temp_image = os.path.join(UPLOAD_FOLDER, 'temp.png')
        fig_data.savefig(temp_image, format='png')

        print("Graphic type is perceived ...")
        chart_type = detect_chart_type(temp_image)

        print("Video is being created ...")
        video_path = os.path.join(OUTPUT_FOLDER, 'temp_video.mp4')
        final_path = os.path.join(OUTPUT_FOLDER, 'final_object.mp4')
        temp_video = matplotlib_to_video(fig_data, video_path, frame_rate, duration, codec)

        print("Voice is being created ...")
        narration = f"This video shows a {chart_type}"
        audio_path = os.path.join(OUTPUT_FOLDER, 'voice_over.mp3')
        add_voice_over(narration, audio_path)

        print("Video and sound are combined ...")
        combine_video_audio(temp_video, audio_path, final_path)

        print("Temporary files are deleted ...")
        os.remove(temp_image)
        os.remove(temp_video)
        os.remove(audio_path)

        print("Video is sent...")
        return send_file(final_path, mimetype='video/mp4', as_attachment=True)
    except Exception as e:
        print(f"Hata oluştu: {str(e)}")
        return jsonify({"error": f"Transaction error: {str(e)}"}), 500

@app.route('/add-to-video', methods=['POST'])
def add_to_video():
    """Add an image, video or matplotlib object to an existing video."""
    if 'video' not in request.files:
        return jsonify({"error": "Video file is missing!"}), 400
    
    video_file = request.files['video']
    if video_file.filename == '':
        return jsonify({"error": "No video file selected!"}), 400
    
    position = request.form.get('position', 'end')  # 'start' or 'end'
    
    # Save the uploaded video
    video_path = os.path.join(UPLOAD_FOLDER, 'temp_input_video.mp4')
    video_file.save(video_path)
    
    try:
        output_path = os.path.join(OUTPUT_FOLDER, 'combined_output.mp4')
        final_path = os.path.join(OUTPUT_FOLDER, 'final_combined.mp4')
        
        # Handle video upload
        if 'second_video' in request.files:
            second_video = request.files['second_video']
            if second_video.filename != '':
                second_video_path = os.path.join(UPLOAD_FOLDER, 'temp_second_video.mp4')
                second_video.save(second_video_path)
                combine_videos(video_path, second_video_path, output_path, position)
                os.remove(second_video_path)
        
        # Handle image upload
        elif 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                image_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
                image_file.save(image_path)
                add_image_to_video(image_path, video_path, output_path, position)
                os.remove(image_path)
        
        # Handle matplotlib object upload
        elif 'object' in request.files:
            obj_file = request.files['object']
            if obj_file.filename != '':
                fig_data = pickle.load(obj_file)
                if not isinstance(fig_data, plt.Figure):
                    return jsonify({"error": "Invalid matplotlib object!"}), 400
                add_matplotlib_to_video(fig_data, video_path, output_path, position)
        else:
            return jsonify({"error": "No content (video/image/object) provided to add!"}), 400
        
        # Add voice narration if provided
        if 'narration' in request.form:
            narration = request.form['narration']
            audio_path = os.path.join(OUTPUT_FOLDER, 'voice_over.mp3')
            add_voice_over(narration, audio_path)
            combine_video_audio(output_path, audio_path, final_path)
            os.remove(audio_path)
            os.remove(output_path)
            result_path = final_path
        else:
            result_path = output_path
        
        # Clean up
        os.remove(video_path)
        
        return send_file(result_path, mimetype='video/mp4', as_attachment=True)
        
    except Exception as e:
        if os.path.exists(video_path):
            os.remove(video_path)
        return jsonify({"error": f"Processing error: {str(e)}"}), 500

@app.route('/insert-into-video', methods=['POST'])
def insert_into_video():
    """ It Adds Image Or Matplotlib Graph From A Certain Second To The Video"""
    if 'video' not in request.files:
        return jsonify({"error": "Video file is missing!"}), 400
    
    video_file = request.files['video']
    if video_file.filename == '':
        return jsonify({"error": "Video not selected!"}), 400
    
    # Take the timing
    start_second = float(request.form.get('start_second', 0))
    duration_seconds = float(request.form.get('duration_seconds', 5))
    
    # Save the video file
    video_path = os.path.join(UPLOAD_FOLDER, 'temp_input_video.mp4')
    video_file.save(video_path)
    
    try:
        output_path = os.path.join(OUTPUT_FOLDER, 'output_with_overlay.mp4')
        final_path = os.path.join(OUTPUT_FOLDER, 'final_output.mp4')
        
        # Image processing
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                image_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
                image_file.save(image_path)
                insert_image_into_video(video_path, image_path, output_path, 
                                     start_second, duration_seconds)
                os.remove(image_path)
        
        # Matplotlib object processing
        elif 'object' in request.files:
            obj_file = request.files['object']
            if obj_file.filename != '':
                fig_data = pickle.load(obj_file)
                if not isinstance(fig_data, plt.Figure):
                    return jsonify({"error": "Invalid matplotlib object!"}), 400
                insert_matplotlib_into_video(video_path, fig_data, output_path,
                                          start_second, duration_seconds)
        else:
            return jsonify({"error": "Image or Matplotlib object was not achieved!"}), 400
        
        # Add Audio Description (Optional)
        if 'narration' in request.form:
            narration = request.form['narration']
            audio_path = os.path.join(OUTPUT_FOLDER, 'voice_over.mp3')
            add_voice_over(narration, audio_path)
            combine_video_audio(output_path, audio_path, final_path)
            os.remove(audio_path)
            os.remove(output_path)
            result_path = final_path
        else:
            result_path = output_path
        
        # Cleaning
        os.remove(video_path)
        
        return send_file(result_path, mimetype='video/mp4', as_attachment=True)
        
    except Exception as e:
        if os.path.exists(video_path):
            os.remove(video_path)
        return jsonify({"error": f"Transaction error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)