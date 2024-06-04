# Audio Loudness Normalization Script

## Introduction
This Python script provides functionalities for calculating Loudness Units Full Scale (LUFS) integrated values and applying Replay Gain adjustments to audio files.

## Features
- Calculate LUFS integrated values for audio files.
- Determine gain adjustments required to reach a target LUFS level.
- Apply Replay Gain adjustments to audio files for loudness normalization.

## Dependencies
- [mutagen](https://mutagen.readthedocs.io/en/latest/)
- [pyloudnorm](https://github.com/csteinmetz1/pyloudnorm)
- [pydub](https://github.com/jiaaro/pydub)
- [soundfile](https://pysoundfile.readthedocs.io/en/0.10.3/)
- [FFmpeg](https://ffmpeg.org/) (required by pydub)

## Installation
You can install the required dependencies using pip:
```bash
pip install mutagen pyloudnorm pydub soundfile
```

## Usage
1. **Calculate LUFS Integrated Value:**
```python
integrated_lufs = calculate_lufs_integrated(input_file)
```

2. **Calculate Gain to Target LUFS:**
```python
target_lufs = -14.0
gain_to_target_lufs = calculate_gain_to_target_lufs(integrated_lufs, target_lufs)
```

3. **Apply Replay Gain to Audio File:**
```python
write_replay_gain_ogg(input_file, gain_to_target_lufs)
```

## Examples
```python
input_file = "input/audio_file.ogg"
integrated_lufs = calculate_lufs_integrated(input_file)
target_lufs = -14.0
gain_to_target_lufs = calculate_gain_to_target_lufs(integrated_lufs, target_lufs)
write_replay_gain_ogg(input_file, gain_to_target_lufs)
```

