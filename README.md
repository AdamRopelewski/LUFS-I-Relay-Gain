# Audio Loudness Normalization Script

## Introduction
This Python script provides functionalities for calculating Loudness Units Full Scale (LUFS) integrated values and applying Replay Gain adjustments to flac audio files.

## Features
- Calculate LUFS integrated values for audio files.
- Determine the gain adjustments required to reach a target LUFS level.
- Apply Replay Gain adjustments to audio files for loudness normalization.

## Dependencies
- [mutagen](https://mutagen.readthedocs.io/en/latest/)
- [pyloudnorm](https://github.com/csteinmetz1/pyloudnorm)
- [pydub](https://github.com/jiaaro/pydub)
- [soundfile](https://python-soundfile.readthedocs.io/)
- [FFmpeg](https://ffmpeg.org/) (required by pydub)

## Installation
1. Clone this repo
2. Install the required dependencies, e.g. using pip:
```bash
pip install mutagen pyloudnorm pydub soundfile
```

## Usage
1. Run python gui.py
2. Select the input directory
3. Select the output directory
4. Enter the Target LUFS value
5. Click on "Process Files"
6. Watch the progress in the status box. 

### Notes:
- Program keeps the file hierarchy.
- Original files will remain unchanged.

### Tips
- You can later use e.g. AIMP to convert flac to lossy formats. I suggest Opus.
    - Remember that you can set the target LUFS e.g. 1 dB higher, and then normalize in the AIMP to avoid clipping due to lossy compression.
- Programs like Tidla-dl or Zotify can be great sources of input audio files.
