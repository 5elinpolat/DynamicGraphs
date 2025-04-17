import matplotlib.pyplot as plt
import requests
import pickle
from io import BytesIO

fig = plt.figure()
plt.plot([0, 1, 2], [0, 1, 0], label="Test")
plt.title("Sample Line Chart")
plt.legend()

buffer = BytesIO()
pickle.dump(fig, buffer)
buffer.seek(0)

files = {'object': ('figure.pkl', buffer, 'application/octet-stream')}
data = {'frame_rate': 15, 'duration': 3}
response = requests.post('http://localhost:5001/upload-object', files=files, data=data)

with open('final_object.mp4', 'wb') as f:
    f.write(response.content)

plt.close(fig)