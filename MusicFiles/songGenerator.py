from pydub import AudioSegment
from pydub.generators import Sine
import numpy as np

def generate_tone(frequency, duration_ms, bpm):
    # Calculate the length of one beat in milliseconds
    beat_length_ms = 60000 / bpm
    # Calculate the number of beats in the duration
    num_beats = int(np.ceil(duration_ms / beat_length_ms))
    # Generate one beat of sound
    beat = Sine(frequency).to_audio_segment(duration=beat_length_ms)
    # Generate silence to follow the beat
    silence = AudioSegment.silent(duration=beat_length_ms)
    # Concatenate the beats and silence to create the pattern
    pattern = beat + silence
    # Trim the pattern to the exact duration required
    tone = pattern * num_beats
    tone = tone[:duration_ms]
    return tone

def create_song(bpm_intervals):
    song = AudioSegment.silent(duration=0)
    for bpm, duration in bpm_intervals:
        frequency = 440  # A4 tone frequency
        tone = generate_tone(frequency, duration * 1000, bpm)
        song += tone
    return song

# Define the BPM intervals and their durations in seconds
bpm_intervals = [(90, 7), (115, 10), (140, 20)]

# Create the song
song = create_song(bpm_intervals)

# Export the song to a file
song.export("output_song2.wav", format="wav")

print("Song generated and saved as output_song.wav")
