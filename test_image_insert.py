import requests

# Prepare Video and Image Files
files = {
    'video': ('main_video.mp4', open('main_video.mp4', 'rb')),
    'image': ('graph.jpg', open('graph.jpg', 'rb'))
}

#Determine when and for how long
data = {
    'start_second': 2,  # Start in 2 second
    'duration_seconds': 5 # Show 5 seconds
}

print("The image is added to the video ...")
response = requests.post('http://localhost:5001/insert-into-video', files=files, data=data)

if response.status_code == 200:
    # Result Save Video
    with open('final_video.mp4', 'wb') as f:
        f.write(response.content)
    print("Video Created successfully: final_video.mp4")
else:
    print(f"Error occurred: {response.json()}") 
