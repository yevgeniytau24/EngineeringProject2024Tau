import pandas as pd
import numpy as np
import random

def generate_random_song_data(num_songs):
    data = []
    for i in range(num_songs):
        song_id = i + 1
        total_duration_seconds = random.randint(120, 315)  # Total duration between 2 and 10 minutes
        total_duration_minutes = total_duration_seconds / 60
        bpm = round(random.uniform(60, 180), 2)  # BPM between 60 and 180
        data.append({
            "Song ID": song_id,
            "Total Duration (minutes)": total_duration_minutes,
            "Total Duration (seconds)": total_duration_seconds,
            "BPM": bpm
        })
    return data

def format_seconds_to_mm_ss(seconds):
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{int(minutes):02}:{int(remaining_seconds):02}"

def save_to_excel(song_data, filename):
    # Convert song data to a format suitable for DataFrame
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

# Generate random song data for 150 songs
num_songs = 300
song_data = generate_random_song_data(num_songs)

# Save the data to an Excel file
filename = "single_bpm_songs_data.xlsx"
save_to_excel(song_data, filename)

print(f"Random song data generated and saved to {filename}")
