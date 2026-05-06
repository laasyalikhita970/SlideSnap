import tkinter as tk
from downloader import download_video
from pdf_converter import images_to_pdf
import threading
import main  # your slide extraction logic

def set_status(text):
    status_label.after(0, lambda: status_label.config(text=text))


def run_process():
    url = entry.get().strip()

    set_status("⏬ Downloading video...")
    try:
        video_file = download_video(url)
    except Exception as exc:
        set_status(f"❌ Download failed: {exc}")
        return

    if not video_file:
        set_status("❌ Download failed: no file returned.")
        return

    set_status("🎥 Extracting slides...")
    result = main.process_video(video_file)
    if result != 0:
        set_status("❌ Extraction failed.")
        return

    set_status("📄 Creating PDF...")
    try:
        images_to_pdf()
    except Exception as exc:
        set_status(f"❌ PDF creation failed: {exc}")
        return

    set_status("✅ Done! Check slides folder")

def start():
    url = entry.get().strip()
    if not url:
        status_label.config(text="❌ Please enter a YouTube URL")
        return

    # run in separate thread so UI doesn't freeze
    threading.Thread(target=run_process, daemon=True).start()

# GUI window
root = tk.Tk()
root.title("SlideSnap")

tk.Label(root, text="Enter YouTube URL:").pack()

entry = tk.Entry(root, width=50)
entry.pack()

tk.Button(root, text="Start", command=start).pack()

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()