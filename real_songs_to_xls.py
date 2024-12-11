import os
import pandas as pd
import librosa
from mutagen.mp3 import MP3


class SongDatabase:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.songs_data = []

    def extract_bpm(self, y, sr):
        # Try the primary method first
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        if tempo == 0:
            # Fallback method
            onset_env = librosa.onset.onset_strength(y=y, sr=sr)  # Corrected call
            tempo = librosa.feature.tempo(onset_envelope=onset_env, sr=sr)[0]
        return tempo

    def process_file(self, file_path, filename):
        try:
            # Load the audio file with librosa
            y, sr = librosa.load(file_path)

            # Extract BPM
            bpm = self.extract_bpm(y, sr)

            # Log the detected BPM
            print(f"Detected BPM for {filename}: {bpm}")

            # Load the audio file with mutagen to get the duration
            audio = MP3(file_path)
            duration_seconds = audio.info.length
            duration_minutes = duration_seconds / 60  # Convert from seconds to minutes

            # Append the song information to the list
            self.songs_data.append({
                "Song ID": filename,
                "Duration (minutes)": duration_minutes,
                "Duration (seconds)": duration_seconds,
                "Duration (f)": duration_seconds,
                "BPM": bpm if bpm > 0 else "Unknown"  # Handle case where BPM is 0
            })
            print(f"Processed file: {filename}")
        except Exception as e:
            print(f"Could not process file {file_path}: {e}")

    def create_database(self):
        # Loop through each file in the folder
        for filename in os.listdir(self.folder_path):
            if filename.endswith(".mp3"):
                file_path = os.path.join(self.folder_path, filename)
                print(f"Processing file: {file_path}")
                self.process_file(file_path, filename)
            else:
                print(f"Ignored file: {filename}")

    def get_songs_data(self):
        return self.songs_data


def save_songs_to_excel(songs_data, output_file_path):
    # Create a DataFrame
    df = pd.DataFrame(songs_data)

    # Save to Excel file
    df.to_excel(output_file_path, index=False)
    print(f"Excel file created at: {output_file_path}")