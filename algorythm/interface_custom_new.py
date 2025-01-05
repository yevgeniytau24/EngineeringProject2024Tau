import tkinter as tk
from tkinter import ttk, messagebox

import librosa
import pandas as pd
import os
import pygame
from tkinter import filedialog, Listbox, PhotoImage, Button, Frame, Label, Scale
import math
import time
from PIL import Image
import matplotlib.colors as mcolors

from algorythm.algorithm_with_custom import select_songs_dynamic_programming

# Initialize global variables
df = None
custom_intervals = []
THRESHOLD = 7.5
SONGS_PATH = "/Users/jennyafren/real_songs_from_data"
pygame.mixer.init()

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import wave

class MusicPlayer:
    def __init__(self, root, selected_songs):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("600x800")

        self.songs = selected_songs['Song ID'].apply(lambda x: os.path.join(SONGS_PATH, f"{x}.wav")).tolist()
        self.current_song = ""
        self.paused = False
        self.current_song_index = 0
        self.start_time = time.time()

        pygame.mixer.init()
        self.setup_ui()

    def setup_ui(self):
        # Song list
        self.songlist = Listbox(self.root, bg="black", fg="lime", font=("Helvetica", 16), width=100, height=10)
        for song in self.songs:
            self.songlist.insert("end", os.path.basename(song))
        self.songlist.pack(pady=10)

        # Currently playing song label
        self.current_song_label = Label(self.root, text="Now Playing: None", font=("Helvetica", 14), fg="white", bg="black")
        self.current_song_label.pack(pady=10)

        # Control buttons
        control_frame = Frame(self.root)
        control_frame.pack(pady=10)

        self.play_button = Button(control_frame, text="Play", command=self.play_song)
        self.pause_button = Button(control_frame, text="Pause", command=self.pause_song)
        self.next_button = Button(control_frame, text="Next", command=self.next_song)
        self.prev_button = Button(control_frame, text="Previous", command=self.prev_song)

        self.play_button.grid(row=0, column=1, padx=5)
        self.pause_button.grid(row=0, column=2, padx=5)
        self.next_button.grid(row=0, column=3, padx=5)
        self.prev_button.grid(row=0, column=0, padx=5)

        # Volume control
        volume_frame = Frame(self.root)
        volume_frame.pack(pady=10)

        volume_label = Label(volume_frame, text="Volume")
        volume_label.pack(side=tk.LEFT)

        volume_slider = Scale(volume_frame, from_=0, to_=100, orient=tk.HORIZONTAL, command=self.set_volume)
        volume_slider.set(50)
        volume_slider.pack(side=tk.LEFT)

        # Spectrogram button
        self.spectrogram_button = Button(self.root, text="Show Spectrogram", command=self.open_spectrogram)
        self.spectrogram_button.pack(pady=10)

    def play_song(self):
        selected_indices = self.songlist.curselection()
        if selected_indices:
            self.current_song_index = selected_indices[0]
            self.current_song = self.songs[self.current_song_index]
            pygame.mixer.music.load(self.current_song)
            pygame.mixer.music.play()
            self.update_now_playing()

    def pause_song(self):
        pygame.mixer.music.pause()
        self.paused = True

    def next_song(self):
        self.current_song_index = (self.current_song_index + 1) % len(self.songs)
        self.play_song()

    def prev_song(self):
        self.current_song_index = (self.current_song_index - 1) % len(self.songs)
        self.play_song()

    def set_volume(self, val):
        volume = float(val) / 100
        pygame.mixer.music.set_volume(volume)

    def update_now_playing(self):
        now_playing = os.path.basename(self.current_song)
        self.current_song_label.config(text=f"Now Playing: {now_playing}")

    def open_spectrogram(self):
        try:
            # Check if a song is selected
            selected_indices = self.songlist.curselection()
            print(f"Selected indices: {selected_indices}")  # Debugging

            if not selected_indices:
                messagebox.showerror("Error", "No song selected. Please select a song.")
                return

            # Get the selected song index and validate it
            selected_index = selected_indices[0]
            print(f"Selected index: {selected_index}")  # Debugging

            if not self.songs or selected_index >= len(self.songs):
                print(f"self.songs: {self.songs}")  # Debugging
                raise IndexError("Selected index is out of range or song list is empty.")

            # Get the file path of the selected song
            current_song = self.songs[selected_index]
            print(f"Selected song path: {current_song}")  # Debugging

            if not os.path.exists(current_song):
                print(f"File not found: {current_song}")  # Debugging
                raise FileNotFoundError(f"File does not exist at path: {current_song}")

            # Create a new spectrogram window
            spectrogram_window = tk.Toplevel(self.root)
            spectrogram_window.title(f"Spectrogram - {os.path.basename(current_song)}")
            spectrogram_window.geometry("800x600")

            # Create spectrogram plot using librosa
            fig, ax = plt.subplots(figsize=(8, 4))
            y, sr = librosa.load(current_song, sr=None)

            if len(y) == 0:
                raise ValueError("Audio signal is empty. The file might be corrupted or unsupported.")

            # Compute spectrogram
            D = np.abs(librosa.stft(y, n_fft=2048, hop_length=512))
            S_db = librosa.amplitude_to_db(D, ref=np.max)

            # Custom colormap
            colors = [(0.1, 0.1, 0.5), (0.5, 0.1, 0.1), (0.9, 0.9, 0.9)]
            n_bins = 500
            cmap_name = 'custom_blue'
            custom_cmap = mcolors.LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)

            # Plot the spectrogram
            librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='log', cmap=custom_cmap, ax=ax)
            ax.set_title("Custom Spectrogram")
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Frequency (Hz)")
            fig.colorbar(ax.images[0], format='%+2.0f dB')

            # Display spectrogram in the new window
            canvas = FigureCanvasTkAgg(fig, master=spectrogram_window)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(fill="both", expand=True)
            canvas.draw()

        except IndexError as ie:
            print(f"IndexError: {ie}")  # Debugging
            messagebox.showerror("Error", f"Index Error: {ie}")
        except FileNotFoundError as fnfe:
            print(f"FileNotFoundError: {fnfe}")  # Debugging
            messagebox.showerror("Error", str(fnfe))
        except ValueError as ve:
            print(f"ValueError: {ve}")  # Debugging
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            print(f"Unexpected error: {e}")  # Debugging
            messagebox.showerror("Error", f"Failed to generate spectrogram: {e}")


# Functionality setup
def load_file():
    global df
    default_file_path = "/Users/jennyafren/PycharmProjects/EngineeringProject2024Tau/single_bpm_songs_data.xlsx"
    try:
        df = pd.read_excel(default_file_path)
        df['BPM'] = df['BPM'].astype(int)
        messagebox.showinfo("Success", "File loaded successfully!")
    except FileNotFoundError:
        messagebox.showerror("Error", f"File not found at path: {default_file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load file: {e}")

def add_custom_interval():
    try:
        bpm_input = custom_bpm_var.get().strip()
        duration_input = custom_duration_var.get().strip()

        if not bpm_input or not duration_input:
            messagebox.showerror("Error", "Both BPM and Duration fields must be filled.")
            return

        bpm = int(bpm_input)
        duration = int(duration_input)
        custom_intervals.append((bpm, duration))
        intervals_text.set(
            intervals_text.get() + f"Interval {len(custom_intervals)}: BPM {bpm}, Duration {duration} minutes\n"
        )
        custom_bpm_var.set("")
        custom_duration_var.set("")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values for BPM and Duration.")

def display_songs_in_table(songs_df, error_msg=""):
    for widget in table_frame.winfo_children():
        widget.destroy()

    if songs_df.empty:
        messagebox.showinfo("Info", "No songs found to display.")
        return

    # Round the "Total Duration (minutes)" column to 2 decimal places
    if "Total Duration (minutes)" in songs_df.columns:
        songs_df["Total Duration (minutes)"] = songs_df["Total Duration (minutes)"].round(2)

    tree = ttk.Treeview(table_frame, columns=list(songs_df.columns), show="headings")
    tree.pack(fill="both", expand=True)

    for col in songs_df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    for _, row in songs_df.iterrows():
        tree.insert("", "end", values=row.tolist())

    if error_msg:
        error_color = "red" if "Error:" in error_msg and "Error: 0.00" not in error_msg else "green"
        error_label = tk.Label(table_frame, text=error_msg, fg=error_color, justify="left")
        error_label.pack(pady=10)

def restart():
    global custom_intervals
    custom_intervals = []
    training_type.set("")
    intensity.set("")
    duration_var.set("")
    bpm_preference.set("")
    intervals_text.set("")
    for widget in table_frame.winfo_children():
        widget.destroy()
    custom_bpm_var.set("")
    custom_duration_var.set("")

def start_training():
    global df
    try:
        if df is None:
            messagebox.showerror("Error", "No dataset loaded. Please load an Excel file first.")
            return

        training = training_type.get()
        # Map the selected training type back to its key in the dictionary
        training_key = next((key for key, value in training_options.items() if value == training), None)

        if training_key not in training_options:
            messagebox.showerror("Error", "Invalid training type.")
            return

        if training_key == "custom":
            if not custom_intervals:
                messagebox.showerror("Error", "No custom intervals defined.")
                return
            selected_songs = pd.DataFrame()
            total_expected_duration = 0
            total_actual_duration = 0

            for i, (bpm, duration) in enumerate(custom_intervals):
                min_bpm = bpm - bpm * (THRESHOLD / 100)
                max_bpm = bpm + bpm * (THRESHOLD / 100)
                interval_songs = df[(df['BPM'] >= min_bpm) & (df['BPM'] <= max_bpm)].copy()

                if interval_songs.empty:
                    messagebox.showinfo("Info", f"No songs found for BPM range: {min_bpm}-{max_bpm}")
                    continue

                interval_selected_songs, total_duration = select_songs_dynamic_programming(interval_songs, duration)
                total_expected_duration += duration
                total_actual_duration += total_duration
                selected_songs = pd.concat([selected_songs, interval_selected_songs], ignore_index=True)

            error_msg = (f"Total Expected Duration: {total_expected_duration} minutes\n"
                         f"Total Actual Duration: {total_actual_duration:.2f} minutes\n"
                         f"Error: {abs(total_expected_duration - total_actual_duration):.2f} minutes")

            display_songs_in_table(selected_songs, error_msg)
            open_music_player(selected_songs)
            return

        intense = int(intensity.get())
        if not (1 <= intense <= intensity_options[training_key]):
            messagebox.showerror("Error", "Invalid intensity level.")
            return

        duration = int(duration_var.get())
        if duration <= 0:
            messagebox.showerror("Error", "Duration must be greater than 0.")
            return

        bpm_preference_choice = bpm_preference.get()
        bpm_preference_value = bpm_preferences.get(bpm_preference_choice, None)
        if bpm_preference_value is None:
            messagebox.showerror("Error", "Invalid BPM preference.")
            return

        bpm_range = training_bpm_ranges_options[training_key][intense - 1]
        filtered_songs = df[(df['BPM'] >= bpm_range[0]) & (df['BPM'] <= bpm_range[1])].copy()

        if filtered_songs.empty:
            messagebox.showinfo("Info", "No songs found in the specified BPM range.")
            return

        selected_songs, total_duration = select_songs_dynamic_programming(filtered_songs, duration)

        # Apply parabolic ordering if the preference is "parabolic-"
        if bpm_preference_value == "parabolic-":
            sorted_bpm = selected_songs.sort_values(by="BPM", ascending=True).reset_index(drop=True)
            midpoint = len(sorted_bpm) // 2
            selected_songs = pd.concat([
                sorted_bpm.iloc[:midpoint],
                sorted_bpm.iloc[midpoint:].sort_values(by="BPM", ascending=False)
            ]).reset_index(drop=True)
        elif bpm_preference_value == "parabolic+":
            sorted_bpm = selected_songs.sort_values(by="BPM", ascending=False).reset_index(drop=True)
            midpoint = len(sorted_bpm) // 2
            selected_songs = pd.concat([
                sorted_bpm.iloc[:midpoint],
                sorted_bpm.iloc[midpoint:].sort_values(by="BPM", ascending=True)
            ]).reset_index(drop=True)
        elif bpm_preference_value == "shuffle":
            selected_songs = selected_songs.sample(frac=1).reset_index(drop=True)
        elif bpm_preference_value == "increased":
            selected_songs = selected_songs.sort_values(by='BPM').reset_index(drop=True)
        elif bpm_preference_value == "decreased":
            selected_songs = selected_songs.sort_values(by='BPM', ascending=False).reset_index(drop=True)

        error_msg = (f"Target Duration: {duration} minutes\n"
                     f"Actual Duration: {total_duration:.2f} minutes\n"
                     f"Error: {abs(duration - total_duration):.2f} minutes")

        display_songs_in_table(selected_songs, error_msg)
        open_music_player(selected_songs)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def open_music_player(selected_songs):
    player_window = tk.Toplevel(root)
    MusicPlayer(player_window, selected_songs)

# UI setup
root = tk.Tk()
root.title("Training Song Selector")
root.geometry("800x600")

# Set application icon
icon_path = "/Users/jennyafren/PycharmProjects/EngineeringProject2024Tau/algorythm/app_icon.png"
try:
    app_icon = tk.PhotoImage(file=icon_path)
    root.iconphoto(True, app_icon)
except Exception as e:
    messagebox.showwarning("Warning", f"Failed to load app icon: {e}")

# Training options
training_options = {
    "running": "Running",
    "walking": "Walking",
    "yoga": "Yoga",
    "gym": "Gym",
    "swimming": "Swimming",
    "cycling": "Cycling",
    "basketball": "Basketball",
    "zumba": "Zumba",
    "squash": "Squash",
    "custom": "Custom"
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
    "shuffle": "shuffle",
    "parabolic-": "parabolic-",
    # "parabolic+": "parabolic+",
    "increased": "increased",
    "decreased": "decreased"
}
training_bpm_ranges_options = {
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

# Input fields
training_label = tk.Label(root, text="Choose Training Type:")
training_label.pack()
training_type = ttk.Combobox(root, values=list(training_options.values()))
training_type.pack(pady=5)

def update_visibility(event):
    if training_type.get() == "Custom":
        intensity_label.pack_forget()
        intensity.pack_forget()
        duration_label.pack_forget()
        duration_entry.pack_forget()
        bpm_label.pack_forget()
        bpm_preference.pack_forget()
        custom_frame.pack(pady=10, fill="x")
        start_button.pack_forget()
        restart_button.pack_forget()
        start_button.pack(pady=10)
    else:
        custom_frame.pack_forget()
        intensity_label.pack()
        intensity.pack()
        duration_label.pack()
        duration_entry.pack()
        bpm_label.pack()
        bpm_preference.pack()
        start_button.pack_forget()
        restart_button.pack_forget()
        start_button.pack(pady=10)
        restart_button.pack(pady=10)

training_type.bind("<<ComboboxSelected>>", update_visibility) #v

# Intensity
intensity_label = tk.Label(root, text="Choose Intensity Level:")
intensity_label.pack()
intensity = ttk.Combobox(root, values=[1, 2, 3, 4])
intensity.pack(pady=5)

# Duration
duration_label = tk.Label(root, text="Enter Duration (minutes):")
duration_label.pack()
duration_var = tk.StringVar()
duration_entry = ttk.Entry(root, textvariable=duration_var)
duration_entry.pack(pady=5)

# BPM Preference
bpm_label = tk.Label(root, text="Choose BPM Preference:")
bpm_label.pack()
bpm_preference = ttk.Combobox(root, values=list(bpm_preferences.keys()))
bpm_preference.pack(pady=5)

# Custom intervals
custom_frame = tk.Frame(root)
custom_bpm_var = tk.StringVar()
custom_duration_var = tk.StringVar()
custom_bpm_label = tk.Label(custom_frame, text="BPM:")
custom_bpm_label.pack(side="left")
custom_bpm_entry = ttk.Entry(custom_frame, textvariable=custom_bpm_var)
custom_bpm_entry.pack(side="left", padx=5)
custom_duration_label = tk.Label(custom_frame, text="Duration (min):")
custom_duration_label.pack(side="left")
custom_duration_entry = ttk.Entry(custom_frame, textvariable=custom_duration_var)
custom_duration_entry.pack(side="left", padx=5)
add_interval_button = ttk.Button(custom_frame, text="Add Interval", command=add_custom_interval)
add_interval_button.pack(side="left", padx=5)

intervals_text = tk.StringVar()
intervals_label = tk.Label(root, textvariable=intervals_text, justify="left", anchor="w")
intervals_label.pack(pady=10, fill="x")

# Buttons
start_button = ttk.Button(root, text="Start Training", command=start_training)
start_button.pack(pady=10)

restart_button = ttk.Button(root, text="Restart", command=restart)
restart_button.pack(pady=10)

# Table to display songs
table_frame = tk.Frame(root)
table_frame.pack(pady=20, fill="both", expand=True)

# Load file
load_file()

root.mainloop()
