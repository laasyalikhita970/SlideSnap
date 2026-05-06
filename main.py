import cv2
import numpy as np
import os
from downloader import download_video

# -----------------------------
# 1. Input video file
# -----------------------------
url = input("Enter YouTube URL: ")
download_video(url)

# download and find downloaded file
try:
    video_file = download_video(url)
except Exception as exc:
    print("Download failed:", exc)
    exit(1)

if not video_file or not os.path.exists(video_file):
    print("Video not found after download!")
    exit(1)

print("Processing:", video_file)

# -----------------------------
# 2. Create slides folder
# -----------------------------
if not os.path.exists("slides"):
    os.makedirs("slides")

# -----------------------------
# 3. Open video
# -----------------------------
cap = cv2.VideoCapture(video_file)

if not cap.isOpened():
    print(f"Error: Could not open video file '{video_file}'")
    exit()

prev_frame = None
count = 0

# Tuning values (based on your testing)
threshold = 600000
frame_skip = 30
frame_id = 0

# -----------------------------
# 4. Process video
# -----------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_id += 1

    # Skip frames for speed
    if frame_id % frame_skip != 0:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Blur to reduce noise
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    if prev_frame is not None:
        diff = cv2.absdiff(prev_frame, gray)
        score = np.sum(diff)

        # Detect slide change
        if score > threshold:
            filename = f"slides/slide_{count}.jpg"
            cv2.imwrite(filename, frame)
            print(f"Saved: {filename}")
            count += 1

    prev_frame = gray

cap.release()

print("\n✅ Slides extraction complete!")
print(f"Total slides saved: {count}")