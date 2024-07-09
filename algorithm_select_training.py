import pandas as pd

# Load the Excel file
file_path = '/Users/jennyafren/PycharmProjects/ElectricalEngineeringProject/single_bpm_songs_data.xlsx'
df = pd.read_excel(file_path)

print("What kind of training are you planning to do?")
training = input().strip().lower()
print("How intense do you want the training to be? (from 1-3, for gym 1-4)")
intense = int(input().strip().lower())
print("How long will you train? (in minutes)")
duration = int(input().strip())

# Define BPM ranges for different training types
training_bpm_ranges = {
    "running": [(120, 150), (150, 180), (160, 200)],
    "walking": [(90, 110), (110, 130), (130, 150)],
    "yoga": [(50, 80), (80, 100), (100, 140)],
    "gym": [(100, 120), (120, 160), (110, 140), (140, 180)],
    "swimming": [(120, 140), (140, 170), (160, 190)],
    "cycling": [(120, 140), (140, 170), (160, 200)],
    "basketball": [(120, 150), (150, 180)],
    "zumba": [(120, 140), (140, 170)],
    "squash": [(140, 160), (160, 180), (180, 200)]
}

# Filter the songs based on training type
if training in training_bpm_ranges:
    bpm_range = training_bpm_ranges[training][intense - 1]
    filtered_songs = df[(df['BPM'] >= bpm_range[0]) & (df['BPM'] <= bpm_range[1])]

    if filtered_songs.empty:
        print("No songs found in the specified BPM range.")
    else:
        # Sort the filtered songs by BPM to ensure BPM increases with each song
        filtered_songs = filtered_songs.sort_values(by='BPM').reset_index(drop=True)

        selected_songs = pd.DataFrame()
        total_duration = 0

        # Determine the number of segments to divide the BPM range into
        num_segments = 10
        bpm_step = (bpm_range[1] - bpm_range[0]) / num_segments

        for segment in range(num_segments):
            min_bpm = bpm_range[0] + segment * bpm_step
            max_bpm = bpm_range[0] + (segment + 1) * bpm_step

            segment_songs = filtered_songs[(filtered_songs['BPM'] >= min_bpm) & (filtered_songs['BPM'] < max_bpm)]
            if not segment_songs.empty:
                song = segment_songs.sample(n=1).iloc[0]  # Select a random song from the segment
                total_duration += song['Total Duration (minutes)']
                selected_songs = pd.concat([selected_songs, song.to_frame().T], ignore_index=True)
                if total_duration >= duration:
                    break

        # Select songs until the total duration is close to the input duration
        for _, song in filtered_songs.iterrows():
            if total_duration + song['Total Duration (minutes)'] > duration + 1:
                continue
            total_duration += song['Total Duration (minutes)']
            selected_songs = pd.concat([selected_songs, song.to_frame().T], ignore_index=True)
            if total_duration >= duration and total_duration - duration < 1:
                break

        if total_duration - duration >= 1:
            # If we exceed the desired duration by 1 minute, try to remove the last song added
            last_song_duration = selected_songs.iloc[-1]['Total Duration (minutes)']
            if total_duration - last_song_duration >= duration and total_duration - last_song_duration - duration < 1:
                total_duration -= last_song_duration
                selected_songs = selected_songs[:-1]

        # Ensure the selected songs cover the entire BPM range
        selected_songs = selected_songs.sort_values(by='BPM').reset_index(drop=True)

        print("Selected Songs for Training:")
        print(selected_songs)
        print(f"Total Duration: {total_duration} minutes")
else:
    print("Invalid training type provided. Please select from running, walking, yoga, or gym.")
