# 🎤 Speech Segmentation from Audio

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python)](https://www.python.org/)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-6.0-007800?logo=ffmpeg)](https://ffmpeg.org/)
[![Nix](https://img.shields.io/badge/Nix-flake--based-41439a?logo=nixos)](https://nixos.org/)

> A Python script to process a video or audio file, automatically detect speech, and segment it into individual audio clips.

## 📋 Table of Contents

- **[🌟 Features](#-features)**
- **[🔧 Technology Stack](#-technology-stack)**
- **[📁 Project Structure](#-project-structure)**
- **[🚀 Quick Start](#-quick-start)**
- **[📦 Output Deliverables](#-output-deliverables)**
- **[🐛 Troubleshooting](#-troubleshooting)**
- **[🤝 Contributing](#-contributing)**
- **[📄 License](#-license)**

## 🌟 Features

### 🔊 Audio Processing
- **Audio Extraction**: Automatically extracts the audio track from a video file (`.mp4`).
- **Standardization**: Converts audio to a standard format (16kHz, mono) for consistent processing.

### 🗣️ Speech Detection
- **VAD (Voice Activity Detection)**: Uses `webrtcvad` to accurately identify timestamps where speech occurs.
- **Timestamp Generation**: Creates a JSON file containing the start and end times for each detected speech segment.

### ✂️ Segmentation
- **Audio Splitting**: Splits the original audio into multiple smaller files based on the detected timestamps.
- **Systematic Naming**: Saves the segmented clips with clear, sequential names (e.g., `segment_01.wav`, `segment_02.wav`).

## 🔧 Technology Stack

- **Primary Language**: Python 3
- **Core Libraries**:
  - `pydub`: For audio manipulation and conversion.
  - `webrtcvad-wheels`: For voice activity detection.
  - `vosk`: Used for its audio processing utilities.
- **System Dependency**: `ffmpeg` for handling audio/video codecs.
- **Environment Management**: `Nix` to provide a reproducible development environment with all necessary dependencies.

## 📁 Project Structure

```
.
├── .gitignore              # Specifies intentionally untracked files to ignore
├── README.md               # This documentation file
├── requirements.txt        # Python package dependencies
├── segments/               # Output directory for segmented audio clips
├── shell.nix               # Nix configuration for the development environment
├── speech_segmentation.py  # The main Python script
├── speech_timestamps.json  # Output JSON with detected speech timestamps
└── video.mp4               # Input video file (to be downloaded)
```

## 🚀 Quick Start

### Prerequisites
- [Nix Package Manager](https://nixos.org/download.html) installed on your system.
- The input video file. Download it from the link below and place it in the project's root directory as `video.mp4`.

**Download Link**: [Video Link](https://drive.google.com/file/d/1EaE8vyJcdQQ_5vjLRrxo6XRCZg-3aFeL/view?usp=sharing)

### Installation & Execution

The project is configured to run in a self-contained environment using Nix.

1.  **Launch the Environment and Run the Script:**
    Open your terminal in the project's root directory and execute the following single command:

    ```bash
    nix-shell shell.nix --run "python3 -m venv .venv && .venv/bin/pip install -r requirements.txt && .venv/bin/python speech_segmentation.py video.mp4"
    ```

    This command performs all the necessary steps:
    1.  It starts a shell with `python3` and `ffmpeg` available.
    2.  It creates a Python virtual environment at `.venv/`.
    3.  It installs the required packages from `requirements.txt` into the virtual environment.
    4.  It runs the main `speech_segmentation.py` script, processing `video.mp4`.

## 📦 Output Deliverables

After the script runs successfully, you will find the following outputs in your project directory:

-   `extracted_audio.wav`: The mono, 16kHz audio track extracted from `video.mp4`.
-   `speech_timestamps.json`: The JSON file containing an array of objects, each with `start` and `end` keys for a speech segment.
-   `segments/`: A directory containing all the final audio clips (e.g., `segment_0.wav`, `segment_1.wav`, etc.).

## 🐛 Troubleshooting

### Nix `fPIC` or `stdenv` Errors
If you encounter errors related to `fPIC` or `stdenv` during the `nix-shell` execution, it might be due to a corrupted Nix store or channel issues. Try running `nix-store --verify --check-contents` or updating your Nix channels.

### `ffmpeg` Not Found
The `nix-shell` command should automatically provide `ffmpeg`. If you run the Python script manually without `nix-shell`, you must ensure `ffmpeg` is installed and available in your system's PATH.

### Python Package Installation Fails
Ensure you are inside the `nix-shell`. The environment provides the necessary build tools for the Python packages. If issues persist, try removing the `.venv` directory and re-running the command.

## 🤝 Contributing

Contributions are welcome! If you have suggestions or want to improve the script, please feel free to:

1.  Fork the repository.
2.  Create a new feature branch (`git checkout -b feature/your-amazing-feature`).
3.  Commit your changes (`git commit -m 'Add some amazing feature'`).
4.  Push to the branch (`git push origin feature/your-amazing-feature`).
5.  Open a Pull Request.

## 📄 License

This project is licensed under the **MIT License**.
