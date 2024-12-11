import pandas as pd
from data_for_algorythm.training_options import *

# Load the Excel file
file_path = '/Users/jennyafren/PycharmProjects/EngineeringProject2024Tau/single_bpm_songs_data.xlsx'
df = pd.read_excel(file_path)

# Ensure BPM is an integer
df['BPM'] = df['BPM'].astype(int)

# Define constants
THRESHOLD = 10  # ±10 BPM threshold

# Get user inputs
print("Choose your training type:")
for key, value in training_options.items():
    print(f"{key}: {value.capitalize()}")

training_choice = int(input("Enter the number corresponding to your training: ").strip())
training = training_options.get(training_choice, None)

if training is None:
    print("Invalid training type provided.")
elif training == "custom":
    intervals = int(input("Enter the number of intervals for your custom training: ").strip())
    custom_intervals = []

    for i in range(intervals):
        bpm = int(input(f"Enter the BPM for interval {i + 1}: ").strip())
        duration = int(input(f"Enter the duration (in minutes) for interval {i + 1}: ").strip())
        custom_intervals.append((bpm, duration))

    # Processing custom intervals
    selected_songs = pd.DataFrame()
    interval_durations = []

    for i, (bpm, duration) in enumerate(custom_intervals):
        min_bpm = bpm - bpm/THRESHOLD
        max_bpm = bpm + bpm/THRESHOLD
        interval_songs = df[(df['BPM'] >= min_bpm) & (df['BPM'] <= max_bpm)].copy()  # Use .copy() to avoid warning
        # print(interval_songs)
        if interval_songs.empty:
            print(f"No songs found for BPM range: {min_bpm}-{max_bpm}")
            interval_durations.append(0)
            continue

        total_duration = 0
        interval_selected_songs = pd.DataFrame()
        # print(interval_selected_songs)

        while total_duration < duration and not interval_songs.empty:
            remaining_duration = duration - total_duration

            # Use .loc to safely assign the new column
            interval_songs.loc[:, 'Duration Difference'] = abs(interval_songs['Total Duration (minutes)'] - remaining_duration)
            closest_song = interval_songs.loc[interval_songs['Duration Difference'].idxmin()]
            # print(closest_song)
            song_duration = closest_song['Total Duration (minutes)']
            # print(closest_song)

            if total_duration + song_duration > duration + 0.5:  # Allow up to 0.5-minute tolerance
                break

            total_duration += song_duration
            # print(total_duration)
            interval_selected_songs = pd.concat([interval_selected_songs, closest_song.to_frame().T], ignore_index=True)
            # print(interval_selected_songs)
            interval_songs = interval_songs.drop(closest_song.name)

        if total_duration > duration:
            last_song = interval_selected_songs.iloc[-1]
            total_duration -= last_song['Total Duration (minutes)']
            interval_selected_songs = interval_selected_songs[:-1]

        selected_songs = pd.concat([selected_songs, interval_selected_songs], ignore_index=True)
        interval_durations.append(total_duration)
        print(
            f"Interval {i + 1}: BPM Range {min_bpm}-{max_bpm}, Target Duration: {duration} minutes, "
            f"Actual Duration: {round(total_duration, 2)} minutes. "
                f"Accuracy: {round((total_duration / duration) * 100, 4)}%"
        )

    print("\nSelected Songs for Custom Training:")
    print(selected_songs)
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
            training_bpm_ranges = training_bpm_ranges_options

#######from here#########
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

                print("Selected Songs for : " + training + "with the bpm: " + str(bpm_range))
                print(selected_songs)
                print(f"Total Duration: {total_duration} minutes")