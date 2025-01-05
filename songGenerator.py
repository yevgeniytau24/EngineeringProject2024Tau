import pandas as pd
import numpy as np
import random
import os
import wave

# Function to generate random song data
def generate_random_song_data(num_songs):
    data = []
    for i in range(num_songs):
        bpm = round(random.uniform(30, 200), 2)  # BPM between 30 and 200
        song_id = f"Song_{i + 1}_BPM_{bpm}"
        total_duration_seconds = random.randint(120, 315)  # Total duration between 2 and 10 minutes
        total_duration_minutes = total_duration_seconds / 60
        data.append({
            "Song ID": song_id,
            "Total Duration (minutes)": total_duration_minutes,
            "Total Duration (seconds)": total_duration_seconds,
            "BPM": bpm
        })
    return data

# Function to format seconds into mm:ss
def format_seconds_to_mm_ss(seconds):
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{int(minutes):02}:{int(remaining_seconds):02}"

# Function to save data to Excel
def save_to_excel(song_data, filename):
    formatted_data = []
    for song in song_data:
        song_id = song["Song ID"]
        total_duration_minutes = song["Total Duration (minutes)"]
        total_duration_seconds = song["Total Duration (seconds)"]
        formatted_data.append({
            "Song ID": song_id,
            "Total Duration (minutes)": total_duration_minutes,
            "Total Duration (seconds)": total_duration_seconds,
            "Total Duration (mm:ss)": format_seconds_to_mm_ss(total_duration_seconds),
            "BPM": song["BPM"]
        })
    df = pd.DataFrame(formatted_data)
    df.to_excel(filename, index=False)

# Function to delete all files in a folder
def delete_all_files_in_folder(folder_path):
    if os.path.exists(folder_path):
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print(f"All files in '{folder_path}' have been deleted.")
    else:
        print(f"The folder '{folder_path}' does not exist. Creating it now.")
        os.makedirs(folder_path)

# Function to generate piano rhythm WAV file
def generate_piano_rhythm(name, duration, bpm, output_dir):
    sample_rate = 44100  # CD-quality audio
    beat_duration = 60 / bpm  # Duration of one beat in seconds
    total_samples = int(sample_rate * duration)

    def generate_chord(frequencies, duration, amplitude=0.3):
        samples = int(sample_rate * duration)
        t = np.linspace(0, duration, samples, endpoint=False)
        chord = sum(np.sin(2 * np.pi * freq * t) for freq in frequencies)
        envelope = np.exp(-5 * t)  # Exponential decay for piano-like effect
        return (chord * envelope * amplitude).astype(np.float32)

    chord_1 = generate_chord([261.63, 329.63, 392.00], beat_duration * 0.8)  # C major
    chord_2 = generate_chord([220.00, 293.66, 349.23], beat_duration * 0.8)  # A minor
    silence = np.zeros(int(sample_rate * (beat_duration * 0.2)))

    pattern = np.concatenate([chord_1, silence, chord_2, silence])
    num_repeats = int(duration / (len(pattern) / sample_rate))
    full_wave = np.tile(pattern, num_repeats)
    full_wave = full_wave[:total_samples]

    full_wave_pcm = (full_wave * 32767).astype(np.int16)

    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{name}.wav")

    with wave.open(file_path, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(full_wave_pcm.tobytes())

    print(f"Saved: {file_path}")

# Function to process Excel data and generate WAV files
def process_excel_and_generate_songs(excel_path, output_dir):
    delete_all_files_in_folder(output_dir)  # Clear the folder before generating new files
    data = pd.read_excel(excel_path)
    for index, row in data.iterrows():
        name = row['Song ID']
        duration = row['Total Duration (seconds)']
        bpm = row['BPM']
        generate_piano_rhythm(name, duration, bpm, output_dir)

# Main script
if __name__ == "__main__":
    # Generate random song data for 352 songs
    num_songs = 358
    song_data = generate_random_song_data(num_songs)

    # Save the data to an Excel file
    excel_filename = "single_bpm_songs_data.xlsx"
    save_to_excel(song_data, excel_filename)
    print(f"Random song data generated and saved to {excel_filename}")

    # Generate WAV files from Excel data
    excel_path = "/Users/jennyafren/PycharmProjects/EngineeringProject2024Tau/single_bpm_songs_data.xlsx"
    output_dir = "/Users/jennyafren/real_songs_from_data"
    process_excel_and_generate_songs(excel_path, output_dir)
