import cv2
import numpy as np
import os
import shutil


def process_video(video_file=None):
    if os.path.exists("slides"):
        shutil.rmtree("slides")

    if video_file is None:
        for file in os.listdir():
            if file.startswith("video") and (file.endswith(".mp4") or file.endswith(".webm")):
                video_file = file
                break

        if video_file is None:
            print("❌ Video file not found!")
            return 1

    if not os.path.exists(video_file):
        print(f"Video file not found: {video_file}")
        return 1

    print("Processing:", video_file)

    os.makedirs("slides", exist_ok=True)

    cap = cv2.VideoCapture(video_file)
    if not cap.isOpened():
        print(f"Error: Could not open video file '{video_file}'")
        return 1

    prev_frame = None
    last_saved = None
    count = 0

    # Tuning values (based on your testing)
    threshold = 600000
    frame_skip = 30
    frame_id = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_id += 1
        if frame_id % frame_skip != 0:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        if prev_frame is not None:
            diff = cv2.absdiff(prev_frame, gray)
            score = np.sum(diff)
            if score > threshold:
                if last_saved is not None:
                    slide_diff = cv2.absdiff(last_saved, gray)
                    slide_score = np.sum(slide_diff)
                    if slide_score < 300000:
                        prev_frame = gray
                        continue

                filename = f"slides/slide_{count}.jpg"
                cv2.imwrite(filename, frame)
                print(f"Saved: {filename}")

                last_saved = gray.copy()
                count += 1

        prev_frame = gray

    cap.release()

    print("\n✅ Slides extraction complete!")
    print(f"Total slides saved: {count}")

    return 0