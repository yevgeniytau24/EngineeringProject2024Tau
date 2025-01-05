import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

# Load the songs data
songs_data = pd.read_excel("/Users/jennyafren/PycharmProjects/EngineeringProject2024Tau/single_bpm_songs_data.xlsx")

# Training options and BPM ranges
training_options = {
    "Running": [(120, 150), (150, 180), (160, 200)],
    "Walking": [(90, 110), (110, 130), (130, 150)],
    "Yoga": [(50, 80), (80, 100), (100, 140)],
    "Gym": [(100, 120), (120, 160), (110, 140), (140, 180)],
    "Swimming": [(120, 140), (140, 170), (160, 190)],
    "Cycling": [(120, 140), (140, 170), (160, 200)],
    "Basketball": [(120, 150), (150, 180)],
    "Zumba": [(120, 140), (140, 170)],
    "Squash": [(120, 150), (150, 180)]
}

bpm_preferences = {
    1: "shuffle",
    2: "parabolic-",
    3: "increased",
    4: "decreased"
}

custom_intervals = []

# Function to get BPM range for training type and intensity
def get_bpm_range(training_type, intensity_level):
    if training_type in training_options:
        return training_options[training_type][intensity_level - 1]  # Level 1, 2, 3, etc.
    return (50, 200)

# Dynamic Programming Algorithm for Song Selection
def select_songs_dynamic_programming(filtered_songs, target_duration):
    filtered_songs['Duration Seconds'] = (filtered_songs['Total Duration (minutes)'] * 60).astype(int)
    target_seconds = int(target_duration * 60)

    dp = [[0] * (target_seconds + 1) for _ in range(len(filtered_songs) + 1)]
    song_selection = [[[] for _ in range(target_seconds + 1)] for _ in range(len(filtered_songs) + 1)]

    for i in range(1, len(filtered_songs) + 1):
        song_duration = filtered_songs.iloc[i - 1]['Duration Seconds']
        for t in range(target_seconds + 1):
            dp[i][t] = dp[i - 1][t]
            song_selection[i][t] = song_selection[i - 1][t][:]

            if t >= song_duration:
                if dp[i - 1][t - song_duration] + song_duration > dp[i - 1][t]:
                    dp[i][t] = dp[i - 1][t - song_duration] + song_duration
                    song_selection[i][t] = song_selection[i - 1][t - song_duration][:]
                    song_selection[i][t].append(filtered_songs.iloc[i - 1])

    return pd.DataFrame(song_selection[-1][-1])

# Function to filter songs based on BPM preference
def filter_songs_by_bpm(bpm_range, bpm_preference):
    min_bpm, max_bpm = bpm_range
    if bpm_preference == "parabolic-":
        return songs_data[(songs_data['BPM'] <= max_bpm) & (songs_data['BPM'] >= min_bpm)].sort_values(by='BPM', ascending=False)
    elif bpm_preference == "increased":
        return songs_data[(songs_data['BPM'] >= min_bpm)].sort_values(by='BPM')
    elif bpm_preference == "decreased":
        return songs_data[(songs_data['BPM'] <= max_bpm)].sort_values(by='BPM', ascending=False)
    return songs_data[(songs_data['BPM'] >= min_bpm) & (songs_data['BPM'] <= max_bpm)]

# Function to handle training selection
def handle_training_get_songs():
    training_type = training_type_var.get()
    intensity = intensity_var.get()
    bpm_preference = bpm_preference_var.get()
    duration = duration_entry.get()

    if not training_type or not intensity or not bpm_preference or not duration:
        messagebox.showerror("Input Error", "Please fill all fields!")
        return

    try:
        duration = float(duration)
        intensity_level = int(intensity.split(" ")[1])
        bpm_range = get_bpm_range(training_type, intensity_level)
        filtered_songs = filter_songs_by_bpm(bpm_range, bpm_preference)
        selected_songs = select_songs_dynamic_programming(filtered_songs, duration)
        display_songs(selected_songs)
        total_selected = selected_songs['Duration Seconds'].sum()
        error_seconds = abs(total_selected - int(duration * 60))
        error_percent = (error_seconds / (duration * 60)) * 100
        messagebox.showinfo("Results", f"Target Duration: {duration} min\nTotal Duration: {total_selected // 60}m {total_selected % 60}s\nError: {error_seconds} sec ({error_percent:.2f}%)")
    except ValueError:
        messagebox.showerror("Input Error", "Invalid duration value.")

# Function to display songs in the table
def display_songs(songs):
    for row in song_table.get_children():
        song_table.delete(row)
    for _, song in songs.iterrows():
        song_table.insert("", "end", values=(song['Song ID'], song['Total Duration (mm:ss)'], song['BPM']))

# Initialize the main application window
root = tk.Tk()
root.title("Training Song Selector")

# Variables
training_type_var = tk.StringVar()
intensity_var = tk.StringVar()
bpm_preference_var = tk.StringVar()

duration_entry = tk.Entry(root)

# UI Components
training_label = tk.Label(root, text="Select Training Type:")
training_label.grid(row=0, column=0, padx=10, pady=5)

training_type_combo = ttk.Combobox(root, textvariable=training_type_var)
training_type_combo["values"] = list(training_options.keys())
training_type_combo.grid(row=0, column=1, padx=10, pady=5)

intensity_label = tk.Label(root, text="Select Intensity:")
intensity_label.grid(row=1, column=0, padx=10, pady=5)

intensity_combo = ttk.Combobox(root, textvariable=intensity_var)
intensity_combo["values"] = ["Level 1", "Level 2", "Level 3"]
intensity_combo.grid(row=1, column=1, padx=10, pady=5)

bpm_preference_label = tk.Label(root, text="Select BPM Preference:")
bpm_preference_label.grid(row=2, column=0, padx=10, pady=5)

bpm_preference_combo = ttk.Combobox(root, textvariable=bpm_preference_var)
bpm_preference_combo["values"] = list(bpm_preferences.values())
bpm_preference_combo.grid(row=2, column=1, padx=10, pady=5)

duration_label = tk.Label(root, text="Enter Duration (minutes):")
duration_label.grid(row=3, column=0, padx=10, pady=5)

duration_entry.grid(row=3, column=1, padx=10, pady=5)

get_songs_button = tk.Button(root, text="Get Songs", command=handle_training_get_songs)
get_songs_button.grid(row=4, column=0, columnspan=2, pady=10)

song_table = ttk.Treeview(root, columns=("ID", "Duration", "BPM"), show="headings")
song_table.heading("ID", text="Song ID")
song_table.heading("Duration", text="Duration")
song_table.heading("BPM", text="BPM")
song_table.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Run the application
root.mainloop()
