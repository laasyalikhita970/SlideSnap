import cv2
import numpy as np
import os
import shutil
import stat
import time


def on_rm_error(func, path, exc_info):
    import errno
    exc_type, exc_value = exc_info[:2]
    if exc_type is PermissionError or exc_value.errno in (errno.EACCES, errno.EPERM):
        os.chmod(path, stat.S_IWRITE)
        func(path)
    else:
        raise


def frame_hash(gray, size=(16, 16)):
    small = cv2.resize(gray, size, interpolation=cv2.INTER_AREA)
    mean = small.mean()
    return (small > mean).astype(np.uint8).flatten()


def process_video(video_file=None, thumbnail_callback=None):
    if os.path.exists("slides"):
        try:
            shutil.rmtree("slides", onerror=on_rm_error)
        except PermissionError:
            print("⚠️ Slides folder in use, retrying...")
            time.sleep(1)
            shutil.rmtree("slides", onerror=on_rm_error)

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
    last_saved_hash = None
    last_saved_frame_id = 0
    count = 0

    # Tuning values (based on your testing)
    threshold = 600000
    slide_threshold = 300000
    min_gap = 60
    frame_skip = 30
    frame_id = 0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_id += 1
        if frame_id % frame_skip != 0:
            continue

        if frame_id % 300 == 0:
            print(f"Processing: {frame_id}/{total_frames}")

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        if prev_frame is not None:
            diff = cv2.absdiff(prev_frame, gray)
            score = np.sum(diff)
            if score > threshold:
                if last_saved is not None:
                    if frame_id - last_saved_frame_id < min_gap:
                        prev_frame = gray
                        continue

                    slide_diff = cv2.absdiff(last_saved, gray)
                    slide_score = np.sum(slide_diff)
                    if slide_score < slide_threshold:
                        prev_frame = gray
                        continue

                    current_hash = frame_hash(gray)
                    if last_saved_hash is not None:
                        hamming = np.count_nonzero(current_hash != last_saved_hash)
                        if hamming < 10:
                            prev_frame = gray
                            continue

                filename = f"slides/slide_{count}.jpg"
                cv2.imwrite(filename, frame)
                print(f"Saved: {filename}")

                if thumbnail_callback:
                    thumbnail_callback(filename)

                last_saved = gray.copy()
                last_saved_hash = frame_hash(gray)
                last_saved_frame_id = frame_id
                count += 1

        prev_frame = gray

    cap.release()

    if count == 0:
        print("⚠️ No slides detected. Try another video.")

    print("\n✅ Slides extraction complete!")
    print(f"Total slides saved: {count}")

    return 0


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python main.py <YouTube URL>")
        sys.exit(1)

    from downloader import download_video

    url = sys.argv[1]
    video_file = download_video(url)
    if not video_file:
        print("❌ Download failed: no file returned")
        sys.exit(1)

    status = process_video(video_file)
    sys.exit(status)

