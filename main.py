import pyloudnorm
from pydub import AudioSegment
from pydub.utils import mediainfo
import os
import soundfile as sf


def write_relay_gain(input_file, output_file, gain):
    # Load the input audio file
    audio = AudioSegment.from_file(input_file, format="ogg")

    # Get the current gain of the audio file
    current_gain = mediainfo(input_file)["tags"]["REPLAYGAIN_GAIN"]

    # Calculate the new gain value
    new_gain = float(current_gain) + gain

    # Set the new gain value in the audio file's metadata
    audio.export(output_file, format="ogg", tags={"REPLAYGAIN_GAIN": str(new_gain)})


def calculate_lufs_integrated(input_file):
    # Load the input audio file
    audio = AudioSegment.from_file(input_file, format="ogg")

    # Export the audio to a temporary WAV file
    temp_wav_file = "temp.wav"
    audio.export(temp_wav_file, format="wav")

    # Calculate the LUFS integrated value
    data, rate = sf.read("temp.wav")  # load audio
    meter = pyloudnorm.Meter(rate)
    integrated_lufs = meter.integrated_loudness(data)

    # Delete the temporary WAV file
    os.remove(temp_wav_file)

    return integrated_lufs


def calculate_gain_to_target_lufs(integrated_lufs, target_lufs):
    gain_to_target_lufs = target_lufs - integrated_lufs
    return gain_to_target_lufs


# Usage example
input_file = "input/1-08 Jorja Smith -  Blue Lights.ogg"
integrated_lufs = calculate_lufs_integrated(input_file)
target_lufs = -14.0
gain_to_target_lufs = calculate_gain_to_target_lufs(integrated_lufs, target_lufs)
print(f"gain_to_target_lufs: {gain_to_target_lufs}")
