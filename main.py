import mutagen.oggopus
import pyloudnorm
from pydub import AudioSegment
from pydub.utils import mediainfo
import os
import soundfile as sf
import mutagen


def calculate_lufs_integrated(input_file):
    # Load the input audio file
    format = mediainfo(input_file)["format_name"]
    audio = AudioSegment.from_file(input_file, format=format)

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


# def write_replay_gain(input_file, output_file, gain):
#     # Load the input audio file
#     format = mediainfo(input_file)["format_name"]
#     audio = AudioSegment.from_file(input_file, format=format)

#     file_tags = mediainfo(input_file)

#     # current_gain = mediainfo(input_file)["TAG"]["replaygain_track_gain"]
#     # new_gain = float(current_gain[:-3]) + gain

#     new_gain = gain
#     new_gain = round(new_gain, 2)
#     file_tags["replaygain_track_gain"] = str(new_gain)
#     file_tags["replaygain_album_gain"] = ""
#     # cover = mediainfo(input_file)["TAG"]["cover"]
#     # cover
#     # Set the new gain value in the audio file's metadata


#     audio.export(output_file, format=format, tags=file_tags, bitrate="320k")
def write_replay_gain_ogg(input_file, gain, output_file=None):
    # Load the OGG file with mutagen
    if output_file is None:
        output_file = input_file
    audio = mutagen.oggopus.OggOpus(input_file)

    # Convert gain to string format expected by ReplayGain tags
    gain_str = f"{gain:+.2f} dB"

    # Set ReplayGain tags
    audio["REPLAYGAIN_TRACK_GAIN"] = gain_str
    audio["REPLAYGAIN_ALBUM_GAIN"] = gain_str

    # Save the modified file
    audio.save(output_file)


def clear_replay_gain_ogg(input_file, output_file=None):
    # Load the OGG file with mutagen
    if output_file is None:
        output_file = input_file

    audio = mutagen.oggopus.OggOpus(input_file)

    # Define possible ReplayGain and R128 tags
    replaygain_tags = [
        "REPLAYGAIN_TRACK_GAIN",
        "REPLAYGAIN_ALBUM_GAIN",
        "REPLAYGAIN_TRACK_PEAK",
        "REPLAYGAIN_ALBUM_PEAK",
        "R128_TRACK_GAIN",
        "R128_ALBUM_GAIN",
    ]

    # Remove these tags if they exist
    for tag in replaygain_tags:
        if tag in audio:
            del audio[tag]

    # Save the modified file
    audio.save(output_file)


input_file = "input/1-08 Jorja Smith -  Blue Lights.ogg"
# clear_replay_gain_ogg(input_file)
integrated_lufs = calculate_lufs_integrated(input_file)
target_lufs = -14.0
gain_to_target_lufs = calculate_gain_to_target_lufs(integrated_lufs, target_lufs)
print(f"gain_to_target_lufs: {gain_to_target_lufs}")

write_replay_gain_ogg(input_file, gain_to_target_lufs)
