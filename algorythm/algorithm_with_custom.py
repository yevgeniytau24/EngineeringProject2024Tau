import pandas as pd
from data_for_algorythm.training_options import *

def select_songs_dynamic_programming(filtered_songs, target_duration):
    # Convert durations to integers (in seconds) to simplify calculations
    filtered_songs['Duration Seconds'] = (filtered_songs['Total Duration (minutes)'] * 60).astype(int)
    target_seconds = int(target_duration * 60)

    # Initialize the DP table
    dp = [[0] * (target_seconds + 1) for _ in range(len(filtered_songs) + 1)]
    song_selection = [[[] for _ in range(target_seconds + 1)] for _ in range(len(filtered_songs) + 1)]

    for i in range(1, len(filtered_songs) + 1):
        song_duration = filtered_songs.iloc[i - 1]['Duration Seconds']
        for t in range(target_seconds + 1):
            # Exclude the current song
            dp[i][t] = dp[i - 1][t]
            song_selection[i][t] = song_selection[i - 1][t][:]

            # Include the current song if it fits
            if t >= song_duration:
                if dp[i - 1][t - song_duration] + song_duration > dp[i][t]:
                    dp[i][t] = dp[i - 1][t - song_duration] + song_duration
                    song_selection[i][t] = song_selection[i - 1][t - song_duration][:]
                    song_selection[i][t].append(i - 1)

    # Backtrack to find the selected songs
    selected_indices = song_selection[len(filtered_songs)][target_seconds]
    selected_songs = filtered_songs.iloc[selected_indices].copy()

    total_duration = dp[len(filtered_songs)][target_seconds] / 60  # Convert back to minutes
    selected_songs.drop(columns=['Duration Seconds'], inplace=True)  # Remove the duration seconds column
    return selected_songs, round(total_duration, 2)

if __name__ == "__main__":
    # Load the Excel file
    file_path = '/Users/jennyafren/PycharmProjects/EngineeringProject2024Tau/single_bpm_songs_data.xlsx'
    df = pd.read_excel(file_path)

    # Ensure BPM is an integer
    df['BPM'] = df['BPM'].astype(int)

    # Define constants
    THRESHOLD = 7.5

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
            min_bpm = bpm - bpm*(THRESHOLD/100)
            max_bpm = bpm + bpm*(THRESHOLD/100)
            interval_songs = df[(df['BPM'] >= min_bpm) & (df['BPM'] <= max_bpm)].copy()  # Use .copy() to avoid warning

            if interval_songs.empty:
                print(f"No songs found for BPM range: {min_bpm}-{max_bpm}")
                interval_durations.append(0)
                continue

            interval_selected_songs, total_duration = select_songs_dynamic_programming(interval_songs, duration)

            selected_songs = pd.concat([selected_songs, interval_selected_songs], ignore_index=True)
            interval_durations.append(total_duration)
            print(
                f"Interval {i + 1}: BPM Range {min_bpm}-{max_bpm}, Target Duration: {duration} minutes, "
                f"Actual Duration: {total_duration:.2f} minutes. "
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
                bpm_range = training_bpm_ranges[training][intense - 1]
                filtered_songs = df[(df['BPM'] >= bpm_range[0]) & (df['BPM'] <= bpm_range[1])].copy()

                if filtered_songs.empty:
                    print("No songs found in the specified BPM range.")
                else:
                    # Handle parabolic preferences
                    # if bpm_preference == "parabolic+":
                    #     sorted_bpm = filtered_songs.sort_values(by="BPM", ascending=False).reset_index(drop=True)
                    #     midpoint = len(sorted_bpm) // 2
                    #     filtered_songs = pd.concat([
                    #         sorted_bpm.iloc[:midpoint],  # First half descending
                    #         sorted_bpm.iloc[midpoint:].sort_values(by="BPM", ascending=True)  # Second half ascending
                    #     ]).reset_index(drop=True)
                    if bpm_preference == "parabolic-":
                        selected_songs, total_duration = select_songs_dynamic_programming(filtered_songs, duration)
                        sorted_bpm = selected_songs.sort_values(by="BPM", ascending=True).reset_index(drop=True)
                        midpoint = len(sorted_bpm) // 2
                        selected_songs = pd.concat([
                            sorted_bpm.iloc[:midpoint],  # First half ascending
                            sorted_bpm.iloc[midpoint:].sort_values(by="BPM", ascending=False)  # Second half descending
                        ]).reset_index(drop=True)
                    elif bpm_preference == "increased":
                        selected_songs, total_duration = select_songs_dynamic_programming(filtered_songs, duration)
                        selected_songs = selected_songs.sort_values(by='BPM').reset_index(drop=True)
                    elif bpm_preference == "decreased":
                        selected_songs, total_duration = select_songs_dynamic_programming(filtered_songs, duration)
                        selected_songs = selected_songs.sort_values(by='BPM', ascending=False).reset_index(drop=True)
                    elif bpm_preference == "shuffle":
                        selected_songs, total_duration = select_songs_dynamic_programming(filtered_songs, duration)
                        if isinstance(selected_songs, pd.DataFrame):
                            selected_songs = selected_songs.sample(frac=1).reset_index(drop=True)  # Shuffle rows in DataFrame

                    # selected_songs, total_duration = select_songs_dynamic_programming(filtered_songs, duration)

                    print("Selected Songs:")
                    print(selected_songs)
                    print(f"Total Duration: {total_duration:.2f} minutes")
                    print(f"Target Duration: {duration:.2f} minutes")
                    print(f"Error: {abs(total_duration - duration):.2f} minutes")
                    print("Error in percents: " + str((1-(total_duration/duration))*100) + "%")
