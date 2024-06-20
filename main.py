import pyloudnorm
from pydub import AudioSegment
from pydub.utils import mediainfo
import os
import soundfile as sf
import mutagen.flac


def calculate_gain_to_target_lufs(integrated_lufs, target_lufs):
    gain_to_target_lufs = target_lufs - integrated_lufs
    return gain_to_target_lufs


def calculate_lufs_integrated(input_file):
    format = mediainfo(input_file)["format_name"]
    audio = AudioSegment.from_file(input_file, format=format)
    temp_wav_file = "temp.wav"
    audio.export(temp_wav_file, format="wav")
    data, rate = sf.read(temp_wav_file)
    meter = pyloudnorm.Meter(rate)
    integrated_lufs = meter.integrated_loudness(data)
    os.remove(temp_wav_file)
    return integrated_lufs


def write_replay_gain_flac(input_file, gain, output_file=None):
    if output_file is None:
        output_file = input_file
    audio = mutagen.flac.FLAC(input_file)
    gain_str = f"{gain:+.2f} dB"
    audio["replaygain_track_gain"] = gain_str
    audio["replaygain_album_gain"] = gain_str
    audio.save(output_file)


def find_flac_files(directory):
    flac_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".flac"):
                rel_path = os.path.relpath(os.path.join(root, file), directory)
                flac_files.append(rel_path)
    return flac_files


def copy_file_to_output(input_file, output_file):
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(input_file, "rb") as f:
        with open(output_file, "wb") as f2:
            f2.write(f.read())
