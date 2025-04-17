import cv2
import numpy as np
from gtts import gTTS
import os
import matplotlib.pyplot as plt
from io import BytesIO

def detect_chart_type(image_path):
    """Görüntüden grafik türünü algılar."""
    try:
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise ValueError("Görüntü okunamadı!")
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
        print(f"Grafik algılama hatası: {e}")
        return "unknown chart"

def image_to_video(image_path, output_path='output_video.mp4', frame_rate=30, duration=5, codec='mp4v'):
    """Görüntüyü videoya çevirir."""
    try:
        frame = cv2.imread(image_path)
        if frame is None:
            raise ValueError("Görüntü okunamadı!")
        height, width, layers = frame.shape
        fourcc = cv2.VideoWriter_fourcc(*codec)
        video_writer = cv2.VideoWriter(output_path, fourcc, frame_rate, (width, height))
        if not video_writer.isOpened():
            raise ValueError("Video yazıcısı açılamadı!")
        total_frames = frame_rate * duration
        for _ in range(total_frames):
            video_writer.write(frame)
        video_writer.release()
        return output_path
    except Exception as e:
        raise RuntimeError(f"Video oluşturma hatası: {e}")

def matplotlib_to_video(fig, output_path='output_video.mp4', frame_rate=30, duration=5, codec='mp4v'):
    """Matplotlib nesnesini videoya çevirir."""
    try:
        fig.canvas.draw()
        frame = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
        frame = frame.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        height, width, layers = frame.shape
        fourcc = cv2.VideoWriter_fourcc(*codec)
        video_writer = cv2.VideoWriter(output_path, fourcc, frame_rate, (width, height))
        if not video_writer.isOpened():
            raise ValueError("Video yazıcısı açılamadı!")
        total_frames = frame_rate * duration
        for _ in range(total_frames):
            video_writer.write(frame)
        video_writer.release()
        plt.close(fig)
        return output_path
    except Exception as e:
        plt.close(fig)
        raise RuntimeError(f"Matplotlib video hatası: {e}")

def add_voice_over(text, output_path='voice_over.mp3'):
    """Metni sese çevirir."""
    try:
        tts = gTTS(text=text, lang='en')
        tts.save(output_path)
        return output_path
    except Exception as e:
        raise RuntimeError(f"Seslendirme hatası: {e}")

def combine_video_audio(video_path, audio_path, output_path='final_output.mp4'):
    """Video ve sesi birleştirir."""
    try:
        cmd = f"ffmpeg -i {video_path} -i {audio_path} -c:v copy -c:a aac {output_path} -y"
        result = os.system(cmd)
        if result != 0:
            raise ValueError("ffmpeg çalışmadı!")
        return output_path
    except Exception as e:
        raise RuntimeError(f"Birleştirme hatası: {e}")