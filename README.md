﻿# 🎬 Video2Clips: Automatic Short Clips Generator

**Video2Clips** is a Python script designed to automatically generate short clips (~3 seconds) from longer videos. It intelligently detects scenes within videos, segments them, and exports these clips neatly into separate folders for easy use. All generated clips are exported without audio, making them ideal for video editing, montages, GIF creation, or social media use.

## ✨ Features

- **Automatic Scene Detection:** Detects scene changes based on content differences, efficiently splitting the video.
- **Short Clips:** Clips are approximately 3 seconds in length, ideal for dynamic edits or quick montages.
- **Silent Clips:** All exported clips have audio removed by default to simplify subsequent editing or sharing.
- **Organized Output:** Each processed video has a dedicated output folder, keeping clips neatly sorted.
- **Customizable Duration:** Easily adjust the minimum and maximum duration for clip creation directly in the script parameters.

## 🚀 Prerequisites

- Python 3.8 or higher
- FFmpeg installed ([Installation Guide](https://ffmpeg.org/download.html))

Install Python dependencies using:

```bash
pip install -r requirements.txt
```

## ⚙️ How to Use

1. Place your original `.mp4` videos into the `input` folder.
2. Run the script using:

```bash
python main.py
```

3. Find your generated short, silent clips organized by video name in the `output` folder.

## 📂 Project Structure

```
Video2Clips/
├── input/                 # Folder for input videos
├── output/                # Folder for output clips
├── main.py                # Main Python script
└── requirements.txt       # Python dependencies
```

## ❤️ Support This Project

If this script helps you, consider supporting its development: 
https://ko-fi.com/markonichan

## 📜 License

Distributed under the MIT License.

