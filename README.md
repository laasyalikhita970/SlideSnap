# 📑 SlideSnap

![Python](https://img.shields.io/badge/Python-3.10-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange)

SlideSnap is a Python-based desktop application that automatically extracts presentation slides from YouTube videos using Computer Vision techniques. It detects slide transitions, removes duplicate frames using image hashing, and generates a clean PDF of extracted slides for easy revision.

---

## 🎯 Features

- Download YouTube videos using `yt-dlp`
- Extract frames using OpenCV
- Detect slide transitions using frame difference analysis
- Remove duplicate or near-duplicate slides using image hashing
- Generate structured PDF from extracted slides
- Simple desktop GUI using Tkinter
- Automatic slide folder creation
- Optimized frame processing for better performance

---

## 🛠️ Tech Stack

- Python
- OpenCV
- NumPy
- Pillow (PIL)
- yt-dlp
- Tkinter

---

## ⚙️ Installation

### 1. Clone the repository

git clone https://github.com/your-username/SlideSnap.git  
cd SlideSnap  

---

### 2. Create virtual environment

python -m venv .venv  

---

### 3. Activate environment

Windows  
.venv\Scripts\activate  

Mac/Linux  
source .venv/bin/activate  

---

### 4. Install dependencies

pip install -r requirements.txt  

---

## 🚀 Run the Project

python ui.py  

---

## 🧠 How It Works

- User enters a YouTube video URL  
- Video is downloaded using `yt-dlp`  
- OpenCV processes video frame-by-frame  
- Frame differences detect slide transitions  
- Duplicate frames are removed using hashing  
- Unique slides are saved in `/slides` folder  
- Slides are converted into a PDF  

---

## 📈 Future Improvements

- OCR-based text extraction from slides  
- Web application version  
- AI-based slide importance ranking  
- Support for local video uploads  
- Export to PowerPoint (.pptx)  
- Cloud deployment  