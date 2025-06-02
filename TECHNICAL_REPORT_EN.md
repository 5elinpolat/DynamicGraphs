# Video Processing and Visual Integration System Technical Report

## 1. Project Purpose and Scope

This project is a web service system aimed at dynamically integrating visual elements (static images and matplotlib graphs) into video content. The system provides users with the ability to enrich video content and incorporate data visualizations into the video stream.

## 2. System Architecture

### 2.1 Core Components

The system consists of three main components:

1. **Web Service (app.py)**
   - Flask-based RESTful API
   - Client request handling and routing
   - File upload and processing management
   - Error handling and security controls

2. **Processing Engine (utils.py)**
   - Video processing functions
   - Image manipulation
   - Matplotlib integration
   - Audio processing and merging

3. **Testing and Sample Usage (test_*.py)**
   - Image insertion examples
   - Matplotlib graph integration
   - API usage examples

### 2.2 File Structure

```
project/
├── app.py              # Main application and API endpoints
├── utils.py            # Helper functions and processing logic
├── test_image_insert.py    # Image insertion test code
├── test_object_insert.py   # Matplotlib graph insertion test code
├── uploads/           # Temporary upload directory
└── outputs/           # Processed video outputs
```

## 3. Technical Details

### 3.1 API Endpoints

#### 3.1.1 /insert-into-video (POST)
- **Purpose**: Adding visual elements to video content
- **Parameters**:
  - video: Main video file
  - image/object: Visual to be added (image or matplotlib object)
  - start_second: Start time (seconds)
  - duration_seconds: Display duration
  - narration: Voice narration (optional)

### 3.2 Video Processing Flow

#### 3.2.1 Image Insertion Process (insert_image_into_video)
```python
def insert_image_into_video(video_path, image_path, output_path, start_second, duration_seconds):
    """
    1. Reading video frames
    2. Overlaying image at specified time interval
    3. Image placement with alpha blending
    4. Creating new video
    """
```

#### 3.2.2 Matplotlib Integration (insert_matplotlib_into_video)
```python
def insert_matplotlib_into_video(video_path, fig, output_path, start_second, duration_seconds):
    """
    1. Converting matplotlib figure to temporary image
    2. Calling image insertion process
    3. Cleaning temporary files
    """
```

### 3.3 Technologies Used

- **OpenCV (cv2)**
  - Video frame processing
  - Image manipulation
  - Alpha blending

- **Matplotlib**
  - Data visualization
  - Graph creation
  - Figure serialization

- **Flask**
  - Web API presentation
  - File management
  - Error handling

## 4. Usage Examples

### 4.1 Image Insertion
```python
# Example of adding an image file to video
files = {
    'video': ('main_video.mp4', open('main_video.mp4', 'rb')),
    'image': ('graph.jpg', open('graph.jpg', 'rb'))
}
data = {
    'start_second': 2,
    'duration_seconds': 5
}
response = requests.post('http://localhost:5001/insert-into-video', files=files, data=data)
```

### 4.2 Matplotlib Graph Insertion
```python
# Example of adding a matplotlib graph to video
plt.figure(figsize=(10, 6))
plt.plot(x, y, 'b-', label='Data')
plt.title('Dynamic Graph')

buffer = BytesIO()
pickle.dump(plt.gcf(), buffer)
buffer.seek(0)

files = {
    'video': ('main_video.mp4', open('main_video.mp4', 'rb')),
    'object': ('graph.pkl', buffer, 'application/octet-stream')
}
```

## 5. Performance and Optimization

### 5.1 Video Processing Optimizations
- Frame-by-frame processing
- Memory management
- Temporary file cleanup
- Parallel processing support

### 5.2 System Requirements
- Python 3.x
- OpenCV
- Matplotlib
- Flask
- FFmpeg
- Sufficient disk space and RAM

## 6. Security Measures

- File extension validation
- Size limitations
- Temporary file management
- Error catching and logging

## 7. Future Developments

- Multiple visual support
- Advanced timing control
- Different visual effect options
- Real-time preview
- Batch processing support

## 8. Installation and Running

### 8.1 Required Package Installation
```bash
pip install flask opencv-python matplotlib gtts numpy
```

### 8.2 Starting the System
```bash
python app.py
```

### 8.3 Running Test Scenarios
```bash
python test_image_insert.py  # Image insertion test
python test_object_insert.py # Matplotlib graph insertion test
```

## 9. Error Handling

- File format checks
- API response codes
- Detailed error messages
- Automatic cleanup mechanisms

## 10. Conclusion

This system successfully accomplishes dynamic visual integration into video content. Thanks to its modular structure and extensible architecture, it is suitable for adding new features. With its performance optimizations and security measures, it is ready for production environment use. 