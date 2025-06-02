import cv2
import numpy as np
from gtts import gTTS
import os
import matplotlib.pyplot as plt
from io import BytesIO

def detect_chart_type(image_path):
    """Detects the type of graphics from the image."""
    try:
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise ValueError("The image could not be read!")
        edges = cv2.Canny(img, 100, 200)

        lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)
        if lines is not None and len(lines) > 5:
            return "line chart"

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        rectangles = [cv2.boundingRect(c) for c in contours]
        if any(50 < r[2] < 200 and 50 < r[3] < 300 for r in rectangles):
            return "bar chart"

        params = cv2.SimpleBlobDetector_Params()
        params.filterByArea = True
        params.minArea = 10
        params.maxArea = 500
        detector = cv2.SimpleBlobDetector_create(params)
        keypoints = detector.detect(img)
        if len(keypoints) > 10:
            return "scatter chart"

        return "unknown chart"
    except Exception as e:
        print(f"Graphic detection error: {e}")
        return "unknown chart"

def image_to_video(image_path, output_path='output_video.mp4', frame_rate=30, duration=5, codec='mp4v'):
    """Turns the image into video."""
    try:
        frame = cv2.imread(image_path)
        if frame is None:
            raise ValueError("The image could not read!")
        height, width, layers = frame.shape
        fourcc = cv2.VideoWriter_fourcc(*codec)
        video_writer = cv2.VideoWriter(output_path, fourcc, frame_rate, (width, height))
        if not video_writer.isOpened():
            raise ValueError("Video Printer Could Not Open!")
        total_frames = frame_rate * duration
        for _ in range(total_frames):
            video_writer.write(frame)
        video_writer.release()
        return output_path
    except Exception as e:
        raise RuntimeError(f"Video oluşturma hatası: {e}")

def matplotlib_to_video(fig, video_path, frame_rate, duration, codec='mp4v'):
    try:
        print("matplotlib_to_video started")
        # Take Figure Dimensions
        fig_width, fig_height = fig.canvas.get_width_height()
        print(f"Figure Dimensions: {fig_width}x{fig_height}")

        # Start video printer
        fourcc = cv2.VideoWriter_fourcc(*codec)
        out = cv2.VideoWriter(video_path, fourcc, frame_rate, (fig_width, fig_height))
        if not out.isOpened():
            raise Exception("Video Printer Could Not Open")

        # For each Frame
        for _ in range(int(frame_rate * duration)):
            print("Frame is being created...")
            fig.canvas.draw()
            # Take RGBA data and convert to RGB
            frame = np.asarray(fig.canvas.buffer_rgba())[:, :, :3]  # Only RGB channels
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            out.write(frame)

        print("Video Printer is closing ...")
        out.release()
        print(f"Video Created: {video_path}")
        return video_path
    except Exception as e:
        print(f"matplotlib_to_video error: {str(e)}")
        raise Exception(f"Matplotlib video error: {str(e)}")

def add_voice_over(text, output_path='voice_over.mp3'):
    """It turns the text into sound."""
    try:
        tts = gTTS(text=text, lang='en')
        tts.save(output_path)
        return output_path
    except Exception as e:
        raise RuntimeError(f"Vocalization error: {e}")

def combine_video_audio(video_path, audio_path, output_path='final_output.mp4'):
    """Combines video and sound."""
    try:
        cmd = f"ffmpeg -i {video_path} -i {audio_path} -c:v copy -c:a aac {output_path} -y"
        result = os.system(cmd)
        if result != 0:
            raise ValueError("FFMPEG did not work!")
        return output_path
    except Exception as e:
        raise RuntimeError(f"Joining error: {e}")

def add_image_to_video(image_path, video_path, output_path='combined_video.mp4', position='end'):
    """Adds an image to an existing video at specified position."""
    try:
        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("The image could not be read!")

        # Read the video
        video = cv2.VideoCapture(video_path)
        if not video.isOpened():
            raise ValueError("Could not open the video!")

        # Get video properties
        fps = int(video.get(cv2.CAP_PROP_FPS))
        frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

        # Resize image to match video dimensions
        image = cv2.resize(image, (frame_width, frame_height))

        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

        if position == 'start':
            # Add image frames for 3 seconds
            for _ in range(int(fps * 3)):
                out.write(image)

        # Copy original video frames
        while True:
            ret, frame = video.read()
            if not ret:
                break
            out.write(frame)

        if position == 'end':
            # Add image frames for 3 seconds
            for _ in range(int(fps * 3)):
                out.write(image)

        video.release()
        out.release()
        return output_path

    except Exception as e:
        raise RuntimeError(f"Error adding image to video: {e}")

def add_matplotlib_to_video(fig, video_path, output_path='combined_video.mp4', position='end'):
    """Adds a matplotlib figure to an existing video at specified position."""
    try:
        # Save matplotlib figure to temporary image
        temp_image = 'temp_matplotlib.png'
        fig.savefig(temp_image)

        # Add the image to video
        result = add_image_to_video(temp_image, video_path, output_path, position)

        # Clean up temporary file
        os.remove(temp_image)
        return result

    except Exception as e:
        if os.path.exists('temp_matplotlib.png'):
            os.remove('temp_matplotlib.png')
        raise RuntimeError(f"Error adding matplotlib figure to video: {e}")

def combine_videos(main_video_path, second_video_path, output_path='combined_video.mp4', position='end'):
    """İki videoyu birleştirir."""
    try:
        # Ana videoyu oku
        main_cap = cv2.VideoCapture(main_video_path)
        if not main_cap.isOpened():
            raise ValueError("Ana video açılamadı!")

        # İkinci videoyu oku
        second_cap = cv2.VideoCapture(second_video_path)
        if not second_cap.isOpened():
            raise ValueError("İkinci video açılamadı!")

        # Video özelliklerini al
        fps = int(main_cap.get(cv2.CAP_PROP_FPS))
        frame_width = int(main_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(main_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Video writer oluştur
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

        # İkinci videoyu ana video boyutuna uyarla
        second_width = int(second_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        second_height = int(second_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        if position == 'start':
            # Önce ikinci videoyu ekle
            while True:
                ret, frame = second_cap.read()
                if not ret:
                    break
                # Frame'i ana video boyutuna ölçekle
                frame = cv2.resize(frame, (frame_width, frame_height))
                out.write(frame)

        # Ana videoyu ekle
        while True:
            ret, frame = main_cap.read()
            if not ret:
                break
            out.write(frame)

        if position == 'end':
            # Sonra ikinci videoyu ekle
            while True:
                ret, frame = second_cap.read()
                if not ret:
                    break
                # Frame'i ana video boyutuna ölçekle
                frame = cv2.resize(frame, (frame_width, frame_height))
                out.write(frame)

        # Kaynakları serbest bırak
        main_cap.release()
        second_cap.release()
        out.release()

        return output_path
    except Exception as e:
        raise RuntimeError(f"Video birleştirme hatası: {e}")

def insert_image_into_video(video_path, image_path, output_path='output_with_image.mp4', 
                          start_second=0, duration_seconds=5):
    """Video adds image from a certain second."""
    try:
        # Open the Video
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError("Video could not open!")

        # Get your video features
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Read Image and Scale to Video Size
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Image could not read!")
        image = cv2.resize(image, (frame_width, frame_height))

        # Calculate the start and finish frames
        start_frame = int(start_second * fps)
        end_frame = start_frame + int(duration_seconds * fps)
        
        # Video Create Writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # If we are in the specified range, show image
            if start_frame <= frame_count < end_frame:
                # Combine Image and Frame (Alpha Blending)
                alpha = 0.7  # Image's opaque
                beta = 1.0 - alpha
                frame = cv2.addWeighted(frame, beta, image, alpha, 0)
            
            out.write(frame)
            frame_count += 1

        cap.release()
        out.release()
        return output_path

    except Exception as e:
        raise RuntimeError(f"Image ekleme hatası: {e}")

def insert_matplotlib_into_video(video_path, fig, output_path='output_with_plot.mp4',
                               start_second=0, duration_seconds=5):
    """Videonya belirli bir saniyeden itibaren matplotlib grafiği ekler."""
    try:
        # Matplotlib figure'ı geçici bir dosyaya kaydet
        temp_image = 'temp_plot.png'
        fig.savefig(temp_image)
        
        # Image ekleme fonksiyonunu çağır
        result = insert_image_into_video(video_path, temp_image, output_path,
                                       start_second, duration_seconds)
        
        # Geçici dosyayı sil
        os.remove(temp_image)
        return result
        
    except Exception as e:
        if os.path.exists('temp_plot.png'):
            os.remove('temp_plot.png')
        raise RuntimeError(f"Matplotlib ekleme hatası: {e}")