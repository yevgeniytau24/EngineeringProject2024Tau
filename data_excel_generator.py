import pandas as pd
import numpy as np
import random

def generate_random_song_data(num_songs):
    data = []
    for i in range(num_songs):
        song_id = i + 1
        num_segments = random.randint(1, 5)  # Random number of BPM segments for each song
        total_duration_seconds = 0
        bpm_changes = []
        start_time = 0
        for _ in range(num_segments):
            duration = random.randint(10, 120)  # Duration between 10 and 120 seconds
            bpm = random.randint(60, 180)  # BPM between 60 and 180
            total_duration_seconds += duration
            end_time = start_time + duration
            bpm_changes.append((duration, bpm, start_time, end_time))
            start_time = end_time
        total_duration_minutes = total_duration_seconds / 60
        data.append({
            "Song ID": song_id,
            "Total Duration (minutes)": total_duration_minutes,
            "Total Duration (seconds)": total_duration_seconds,
            "BPM Changes": bpm_changes
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
        for duration, bpm, start_time, end_time in song["BPM Changes"]:
            formatted_data.append({
                "Song ID": song_id,
                "Total Duration (minutes)": total_duration_minutes,
                "Total Duration (seconds)": total_duration_seconds,
                "Segment Duration (seconds)": duration,
                "Segment Duration (mm:ss)": format_seconds_to_mm_ss(duration),
                "Start Time (mm:ss)": format_seconds_to_mm_ss(start_time),
                "End Time (mm:ss)": format_seconds_to_mm_ss(end_time),
                "BPM": bpm
            })

    df = pd.DataFrame(formatted_data)
    df.to_excel(filename, index=False)

# Generate random song data for 150 songs
num_songs = 1500
song_data = generate_random_song_data(num_songs)

# Save the data to an Excel file
filename = "random_songs_data.xlsx"
save_to_excel(song_data, filename)

print(f"Random song data generated and saved to {filename}")
