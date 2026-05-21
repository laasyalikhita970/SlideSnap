# SlideSnap

SlideSnap is a Python-based desktop application that automatically extracts presentation slides from YouTube videos using Computer Vision techniques. The application detects slide changes, removes duplicate frames, and generates a clean PDF containing the extracted slides.

---

## Features

- Download YouTube videos using yt-dlp
- Extract slides from videos using OpenCV
- Detect slide transitions automatically
- Remove duplicate or near-identical slides
- Generate PDF from extracted slides
- Simple desktop GUI using Tkinter
- Automatic slide folder generation
- Frame difference based slide detection
- Duplicate filtering using image hashing

---

## Tech Stack

- Python
- OpenCV
- NumPy
- Tkinter
- Pillow
- yt-dlp

---

## Project Structure

```plaintext
SlideSnap/
│
├── ui.py
├── main.py
├── downloader.py
├── pdf_converter.py
├── README.md
│
├── slides/
│   ├── slide_0.jpg
│   ├── slide_1.jpg
│   └── ...
│
├── slides.pdf
└── .venv/
```

---

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/your-username/slidesnap.git
cd slidesnap
```

---

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

---

### 3. Activate Virtual Environment

#### Windows

```bash
.venv\Scripts\activate
```

#### Mac/Linux

```bash
source .venv/bin/activate
```

---

### 4. Install Dependencies

```bash
pip install opencv-python numpy pillow yt-dlp
```

---

## Run the Application

```bash
python ui.py
```

---

## How It Works

1. User enters a YouTube video URL
2. yt-dlp downloads the video locally
3. OpenCV processes the video frame-by-frame
4. Consecutive frames are compared
5. Large visual differences are treated as slide transitions
6. Duplicate slides are filtered using image comparison and hashing
7. Slides are saved inside the `slides/` folder
8. Extracted slides are converted into a PDF

---

## Output

### Extracted Slides

```plaintext
slides/
```

### Generated PDF

```plaintext
slides.pdf
```

---

## Example Workflow

```plaintext
YouTube URL
      ↓
Video Download
      ↓
Frame Processing
      ↓
Slide Detection
      ↓
Duplicate Removal
      ↓
PDF Generation
```

---

## Future Improvements

- Support for local video file upload
- OCR text extraction from slides
- Improved UI design
- AI-based slide detection
- Web application version
- Export slides as PowerPoint

---

## Challenges Faced

- Detecting meaningful slide transitions
- Removing duplicate slides
- Handling YouTube download restrictions
- Optimizing frame processing speed

---

## Learning Outcomes

Through this project, I learned:

- Computer Vision basics using OpenCV
- Video frame processing
- Image comparison techniques
- GUI development with Tkinter
- File handling in Python
- PDF generation using Pillow

---

## Author

Developed by Laasya Likhita