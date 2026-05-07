import os
import tkinter as tk
from PIL import Image, ImageTk
from downloader import download_video
from pdf_converter import images_to_pdf
import threading
import main  # your slide extraction logic

logo_image = None

def load_logo(size=(52, 52)):
    global logo_image
    for filename in ("logo.png", "logo.webp", "logo.jpg", "logo.jpeg"):
        if os.path.exists(filename):
            try:
                img = Image.open(filename).convert("RGBA")
                img.thumbnail(size, Image.ANTIALIAS)
                logo_image = ImageTk.PhotoImage(img)
                return logo_image
            except Exception:
                continue
    return None

def set_status(text):
    status_label.after(0, lambda: status_label.config(text=text))


def update_thumbnail(image_path):
    try:
        img = Image.open(image_path)
        img.thumbnail((200, 150))
        photo = ImageTk.PhotoImage(img)
        thumbnail_label.config(image=photo)
        thumbnail_label.image = photo
    except Exception:
        pass


def run_process():
    if mode.get() == "url":
        url = entry.get().strip()
        if not url:
            set_status("❌ Please enter a YouTube URL")
            return

        set_status("⏬ Downloading video...")
        try:
            video_file = download_video(url)
        except Exception as exc:
            set_status(f"❌ Download failed: {exc}")
            return

        if not video_file:
            set_status("❌ Download failed: no file returned.")
            return
    else:
        video_file = entry.get().strip()
        if not video_file or not os.path.exists(video_file):
            set_status("❌ Please select a valid video file")
            return

    set_status("🎥 Extracting slides...")
    try:
        result = main.process_video(video_file, update_thumbnail)
    except Exception as exc:
        set_status(f"❌ Extraction error: {exc}")
        return

    if result != 0:
        set_status("❌ Extraction failed.")
        return

    set_status("✅ Extraction complete. Use Open PDF to review slides.")
    pdf_button.config(state="normal")
    try:
        os.startfile("slides")
    except Exception:
        pass

def start():
    threading.Thread(target=run_process, daemon=True).start()


def open_pdf():
    set_status("📄 Generating PDF...")
    try:
        images_to_pdf()
        pdf_path = "slides.pdf"
        if os.path.exists(pdf_path):
            os.startfile(pdf_path)
            set_status("✅ PDF opened.")
        else:
            set_status("⚠️ No slides found to create PDF.")
    except Exception as exc:
        set_status(f"❌ PDF error: {exc}")


def on_mode_change():
    if mode.get() == "url":
        label.config(text="Enter YouTube URL:")
    else:
        label.config(text="Enter local video file path:")

# GUI window
root = tk.Tk()
root.title("SlideSnap")
root.configure(bg="#f4f6f8")
root.geometry("580x580")
root.resizable(False, False)

logo_photo = load_logo()
if logo_photo:
    try:
        root.iconphoto(True, logo_photo)
    except Exception:
        pass

main_frame = tk.Frame(root, bg="#ffffff", padx=24, pady=24)
main_frame.place(relx=0.5, rely=0.5, anchor="center")

mode = tk.StringVar(value="url")

logo_photo = load_logo()
if logo_photo:
    logo_label = tk.Label(main_frame, image=logo_photo, bg="#ffffff")
    logo_label.image = logo_photo
else:
    logo_label = tk.Label(
        main_frame,
        text="📽️",
        font=("Segoe UI Emoji", 28),
        bg="#ffffff"
    )
logo_label.grid(row=0, column=0, padx=(0, 8), sticky="e")

header_label = tk.Label(
    main_frame,
    text="SlideSnap",
    font=("Segoe UI", 22, "bold"),
    fg="#2c3e50",
    bg="#ffffff"
)
header_label.grid(row=0, column=1, columnspan=2, sticky="w")

subtitle_label = tk.Label(
    main_frame,
    text="Extract slides from YouTube or a local video file",
    font=("Segoe UI", 10),
    fg="#556068",
    bg="#ffffff"
)
subtitle_label.grid(row=1, column=0, columnspan=3, pady=(0, 16))

mode_frame = tk.Frame(main_frame, bg="#ffffff")
mode_frame.grid(row=2, column=0, columnspan=3, pady=(0, 18))

tk.Radiobutton(
    mode_frame,
    text="YouTube URL",
    variable=mode,
    value="url",
    command=on_mode_change,
    bg="#ffffff",
    font=("Segoe UI", 10)
).pack(side="left", padx=8)

tk.Radiobutton(
    mode_frame,
    text="Local File",
    variable=mode,
    value="file",
    command=on_mode_change,
    bg="#ffffff",
    font=("Segoe UI", 10)
).pack(side="left", padx=8)

label = tk.Label(main_frame, text="Enter YouTube URL:", font=("Segoe UI", 10), bg="#ffffff")
label.grid(row=3, column=0, columnspan=3, sticky="w", pady=(0, 6))

entry = tk.Entry(main_frame, width=44, font=("Segoe UI", 10), bd=1, relief="solid")
entry.grid(row=4, column=0, columnspan=3, sticky="ew", pady=(0, 12))

start_button = tk.Button(
    main_frame,
    text="Start",
    command=start,
    bg="#4a90e2",
    fg="#ffffff",
    activebackground="#357ABD",
    activeforeground="#ffffff",
    bd=0,
    padx=18,
    pady=10,
    font=("Segoe UI", 11, "bold")
)
start_button.grid(row=5, column=0, columnspan=3, pady=(0, 14), sticky="ew")

pdf_button = tk.Button(
    main_frame,
    text="Open PDF",
    command=lambda: open_pdf(),
    bg="#34a853",
    fg="#ffffff",
    activebackground="#2c7d3f",
    activeforeground="#ffffff",
    bd=0,
    padx=18,
    pady=10,
    font=("Segoe UI", 11, "bold"),
    state="disabled"
)
pdf_button.grid(row=6, column=0, columnspan=3, pady=(0, 18), sticky="ew")

status_label = tk.Label(main_frame, text="", font=("Segoe UI", 12), fg="#333333", bg="#ffffff", wraplength=460, justify="center")
status_label.grid(row=7, column=0, columnspan=3, pady=(0, 12))

thumbnail_label = tk.Label(
    main_frame,
    text="Slide preview will appear here",
    font=("Segoe UI", 10),
    fg="#7f8c8d",
    bg="#ecf0f1",
    width=42,
    height=11,
    bd=1,
    relief="solid",
    anchor="center",
    justify="center"
)
thumbnail_label.grid(row=8, column=0, columnspan=3)

on_mode_change()

root.mainloop()