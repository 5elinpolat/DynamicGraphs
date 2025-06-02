import matplotlib.pyplot as plt
import requests
import pickle
from io import BytesIO
import numpy as np

# Create Matplotlib graph
plt.figure(figsize=(10, 6))

# Sample data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Draw the graph
plt.plot(x, y, 'b-', label='Sinüs Dalgası')
plt.title('Dinamik Grafik')
plt.xlabel('Zaman')
plt.ylabel('Genlik')
plt.grid(True)
plt.legend()

# Serialize the graph with pickle
buffer = BytesIO()
pickle.dump(plt.gcf(), buffer)
buffer.seek(0)

# Prepare Video and Matplotlib object
files = {
    'video': ('main_video.mp4', open('main_video.mp4', 'rb')),
    'object': ('graph.pkl', buffer, 'application/octet-stream')
}

# Determine when and for how long the graph will be displayed
data = {
    'start_second': 3,  #Start in 3rd second
    'duration_seconds': 4, # Show 4 seconds
    'narration': 'This graph shows a sine wave pattern'  # Optional Sound Description
}

print("Graphic is added to the video ...")
response = requests.post('http://localhost:5001/insert-into-video', files=files, data=data)

if response.status_code == 200:
    # Result Save Video
    with open('video_with_plot.mp4', 'wb') as f:
        f.write(response.content)
    print("Video Created successfully: video_with_plot.mp4")
else:
    print(f"Error occurred: {response.json()}")

# Turn off the matplotlib window
plt.close() 
