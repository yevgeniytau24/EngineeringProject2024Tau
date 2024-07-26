import os
import pandas as pd
import librosa
from mutagen.mp3 import MP3

# make a real database of song we have!

# Define the path to the folder containing your MP3 files
folder_path = '/Users/jennyafren/PycharmProjects/ElectricalEngineeringProject/MusicFiles'

# Initialize an empty list to store song information
songs_data = []


# Function to extract BPM
def extract_bpm(y, sr):
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    return tempo


# Loop through each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".mp3"):
        file_path = os.path.join(folder_path, filename)

        try:
            # Load the audio file with librosa
            y, sr = librosa.load(file_path)

            # Extract BPM
            bpm = extract_bpm(y, sr)

            # Load the audio file with mutagen to get the duration
            audio = MP3(file_path)
            duration_seconds = audio.info.length
            duration_minutes = duration_seconds / 60  # Convert from seconds to minutes

            # Append the song information to the list
            songs_data.append({
                "Song ID": filename,
                "Duration (minutes)": duration_minutes,
                "Duration (seconds)": duration_seconds,
                "Duration (f)": duration_seconds,
                "BPM": bpm
            })
        except Exception as e:
            print(f"Could not process file {file_path}: {e}")

# Create a DataFrame
df = pd.DataFrame(songs_data)

# Save to Excel file
output_file_path = '/Users/jennyafren/PycharmProjects/EngineeringProject2024Tau/songs_data.xlsx'
df.to_excel(output_file_path, index=False)

print(f"Excel file created at: {output_file_path}")