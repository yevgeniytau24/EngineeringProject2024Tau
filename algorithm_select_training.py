import pandas as pd

# Load the Excel file
file_path = '/Users/jennyafren/PycharmProjects/ElectricalEngineeringProject/single_bpm_songs_data.xlsx'
df = pd.read_excel(file_path)

# Mapping numbers to training types and preferences
training_options = {
    1: "running",
    2: "walking",
    3: "yoga",
    4: "gym",
    5: "swimming",
    6: "cycling",

    7: "basketball",
    8: "zumba",
    9: "squash"
}

intensity_options = {
    "running": 3,
    "walking": 3,
    "yoga": 3,
    "gym": 4,
    "swimming": 3,
    "cycling": 3,
    "basketball": 2,
    "zumba": 2,
    "squash": 3
}

bpm_preferences = {
    1: "shuffle",
    2: "parabolic+",
    3: "parabolic-",
    4: "increased",
    5: "decreased"
}

# Get user inputs
print("Choose your training type:")
for key, value in training_options.items():
    print(f"{key}: {value.capitalize()}")

training_choice = int(input("Enter the number corresponding to your training: ").strip())
training = training_options.get(training_choice, None)

if training is None:
    print("Invalid training type provided.")
else:
    max_intensity = intensity_options[training]
    print(f"How intense do you want the training to be? (from 1-{max_intensity})")
    intense = int(input().strip())

    if not (1 <= intense <= max_intensity):
        print("Invalid intensity level provided.")
    else:
        print("How long will you train? (in minutes)")
        duration = int(input().strip())

        print("Choose your BPM preference:")
        for key, value in bpm_preferences.items():
            print(f"{key}: {value.capitalize()}")

        bpm_preference_choice = int(input("Enter the number corresponding to your BPM preference: ").strip())
        bpm_preference = bpm_preferences.get(bpm_preference_choice, None)

        if bpm_preference is None:
            print("Invalid BPM preference provided.")
        else:
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

            bpm_range = training_bpm_ranges[training][intense - 1]
            filtered_songs = df[(df['BPM'] >= bpm_range[0]) & (df['BPM'] <= bpm_range[1])]

            if filtered_songs.empty:
                print("No songs found in the specified BPM range.")
            else:
                if bpm_preference == "increased":
                    filtered_songs = filtered_songs.sort_values(by='BPM').reset_index(drop=True)
                elif bpm_preference == "decreased":
                    filtered_songs = filtered_songs.sort_values(by='BPM', ascending=False).reset_index(drop=True)
                elif bpm_preference == "parabolic+":
                    midpoint = len(filtered_songs) // 2
                    first_half = filtered_songs.iloc[:midpoint].sort_values(by='BPM').reset_index(drop=True)
                    second_half = filtered_songs.iloc[midpoint:].sort_values(by='BPM', ascending=False).reset_index(drop=True)
                    filtered_songs = pd.concat([first_half, second_half]).reset_index(drop=True)
                elif bpm_preference == "parabolic-":
                    midpoint = len(filtered_songs) // 2
                    first_half = filtered_songs.iloc[:midpoint].sort_values(by='BPM', ascending=False).reset_index(drop=True)
                    second_half = filtered_songs.iloc[midpoint:].sort_values(by='BPM').reset_index(drop=True)
                    filtered_songs = pd.concat([first_half, second_half]).reset_index(drop=True)
                elif bpm_preference == "shuffle":
                    filtered_songs = filtered_songs.sample(frac=1).reset_index(drop=True)

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
                if bpm_preference == "increased":
                    selected_songs = selected_songs.sort_values(by='BPM').reset_index(drop=True)
                elif bpm_preference == "decreased":
                    selected_songs = selected_songs.sort_values(by='BPM', ascending=False).reset_index(drop=True)
                elif bpm_preference == "parabolic+":
                    selected_songs = pd.concat([selected_songs.iloc[:len(selected_songs)//2].sort_values(by='BPM'),
                                                selected_songs.iloc[len(selected_songs)//2:].sort_values(by='BPM', ascending=False)]).reset_index(drop=True)
                elif bpm_preference == "parabolic-":
                    selected_songs = pd.concat([selected_songs.iloc[:len(selected_songs)//2].sort_values(by='BPM', ascending=False),
                                                selected_songs.iloc[len(selected_songs)//2:].sort_values(by='BPM')]).reset_index(drop=True)
                elif bpm_preference == "shuffle":
                    selected_songs = selected_songs.sample(frac=1).reset_index(drop=True)

                print("Selected Songs for Training:")
                print(selected_songs)
                print(f"Total Duration: {total_duration} minutes")