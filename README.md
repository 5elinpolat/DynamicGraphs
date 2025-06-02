# Video Processing and Visual Integration System

A Flask-based web service that allows you to dynamically integrate visual elements (images and matplotlib graphs) into video content at specific time points.

## Features

- Insert static images into videos at specific timestamps
- Add matplotlib graphs into videos with customizable timing
- Optional voice-over narration support
- Semi-transparent overlay of visuals (alpha blending)
- Automatic image scaling to match video dimensions
- Temporary file management and cleanup

## Project Structure

```
project/
├── app.py                  # Main Flask application
├── utils.py               # Core processing functions
├── test_image_insert.py   # Image insertion example
├── test_object_insert.py  # Matplotlib graph insertion example
├── uploads/              # Temporary upload directory
└── outputs/              # Processed video outputs
```

## Requirements

- Python 3.x
- OpenCV (cv2)
- Flask
- Matplotlib
- gTTS (Google Text-to-Speech)
- FFmpeg
- NumPy

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Install required packages:
```bash
pip install flask opencv-python matplotlib gtts numpy
```

3. Install FFmpeg:
   - For macOS: `brew install ffmpeg`
   - For Ubuntu: `sudo apt-get install ffmpeg`
   - For Windows: Download from the official FFmpeg website

## Usage

### 1. Start the Server

```bash
python app.py
```
The server will start on `http://localhost:5001`

### 2. Insert an Image into a Video

```python
# Using test_image_insert.py
files = {
    'video': ('main_video.mp4', open('main_video.mp4', 'rb')),
    'image': ('graph.jpg', open('graph.jpg', 'rb'))
}
data = {
    'start_second': 2,    # Start at 2 seconds
    'duration_seconds': 5  # Show for 5 seconds
}
response = requests.post('http://localhost:5001/insert-into-video', files=files, data=data)
```

### 3. Insert a Matplotlib Graph into a Video

```python
# Using test_object_insert.py
plt.figure(figsize=(10, 6))
plt.plot([1, 2, 3, 4], [1, 4, 2, 3])
plt.title("Dynamic Graph")

buffer = BytesIO()
pickle.dump(plt.gcf(), buffer)
buffer.seek(0)

files = {
    'video': ('main_video.mp4', open('main_video.mp4', 'rb')),
    'object': ('graph.pkl', buffer, 'application/octet-stream')
}
data = {
    'start_second': 3,
    'duration_seconds': 4,
    'narration': 'This graph shows our data trend'
}
response = requests.post('http://localhost:5001/insert-into-video', files=files, data=data)
```

## API Endpoints

### POST /insert-into-video

Add a visual element to a video.

**Parameters:**
- `video`: Main video file (multipart/form-data)
- `image` or `object`: Visual element to insert (image file or serialized matplotlib object)
- `start_second`: When to start showing the visual (in seconds)
- `duration_seconds`: How long to show the visual
- `narration`: Optional voice-over text

**Response:**
- Success: Video file (video/mp4)
- Error: JSON with error message

## Testing

Two test scripts are provided:

1. `test_image_insert.py`: Demonstrates inserting an image into a video
2. `test_object_insert.py`: Shows how to add a matplotlib graph to a video

Run the tests:
```bash
python test_image_insert.py
python test_object_insert.py
```

## Error Handling

The system includes comprehensive error handling for:
- File format validation
- Video processing errors
- Resource cleanup
- API response codes

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Technical Documentation

For detailed technical information, see:
- [Technical Report](TECHNICAL_REPORT_EN.md)
