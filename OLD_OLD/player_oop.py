import pandas as pd
import tkinter as tk
from tkinter import filedialog, Menu, Listbox, Button, Label, Scale, Frame, PhotoImage
import pygame
import os
import math
import time


class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("400x700")

        pygame.mixer.init()
        self.songs = []
        self.current_song = ""
        self.paused = False
        self.start_time = time.time()
        self.selected_songs = None
        self.current_song_index = 0

        self.setup_ui()

    def setup_ui(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        organise_menu = Menu(menubar, tearoff=False)
        organise_menu.add_command(label='Select Folder', command=self.load_music)
        menubar.add_cascade(label='Organize', menu=organise_menu)

        self.songlist = Listbox(self.root, bg="black", fg="lime", font=("Helvetica", 16), width=100, height=15)
        self.songlist.pack()

        self.play_btn_img = PhotoImage(
            file='/Users/jennyafren/PycharmProjects/ElectricalEngineeringProject/nplay button_player_icon.png')
        self.pause_btn_img = PhotoImage(
            file='/Users/jennyafren/PycharmProjects/ElectricalEngineeringProject/npause_player_icon.png')
        self.next_btn_img = PhotoImage(
            file='/Users/jennyafren/PycharmProjects/ElectricalEngineeringProject/nnext_player_icon.png')
        self.prev_btn_img = PhotoImage(
            file='/Users/jennyafren/PycharmProjects/ElectricalEngineeringProject/nprevious_icon.png')

        control_frame = Frame(self.root)
        control_frame.pack()

        self.play_btn = Button(control_frame, image=self.play_btn_img, borderwidth=0, command=self.play_music)
        self.pause_btn = Button(control_frame, image=self.pause_btn_img, borderwidth=0, command=self.pause_music)
        self.next_btn = Button(control_frame, image=self.next_btn_img, borderwidth=0, command=self.next_music)
        self.prev_btn = Button(control_frame, image=self.prev_btn_img, borderwidth=0, command=self.prev_music)

        self.play_btn.grid(row=0, column=2, padx=7, pady=10)
        self.pause_btn.grid(row=0, column=1, padx=7, pady=10)
        self.next_btn.grid(row=0, column=3, padx=7, pady=10)
        self.prev_btn.grid(row=0, column=0, padx=7, pady=10)

        volume_frame = Frame(self.root)
        volume_frame.pack(pady=10)

        volume_label = Label(volume_frame, text="Volume")
        volume_label.pack(side=tk.LEFT)

        volume_slider = Scale(volume_frame, from_=0, to_=100, orient=tk.HORIZONTAL, command=self.set_volume)
        volume_slider.set(50)
        volume_slider.pack(side=tk.LEFT)

        self.timer_label = Label(self.root, text="00:00", font=("Helvetica", 16), bg="black", fg="lime")
        self.timer_label.pack(pady=10)

        self.canvas = tk.Canvas(self.root, bg="black", width=400, height=200)
        self.canvas.pack(pady=10)

        self.update_visual_effect()

    def load_music(self):
        self.root.directory = "/Users/jennyafren/PycharmProjects/ElectricalEngineeringProject/MusicFiles"

        if not os.path.isdir(self.root.directory):
            self.root.directory = filedialog.askdirectory()

        self.songs = []
        for song in os.listdir(self.root.directory):
            name, ext = os.path.splitext(song)
            if ext == ".mp3":
                self.songs.append(song)
        for song in self.songs:
            self.songlist.insert("end", song)

        if self.songs:
            self.songlist.selection_set(0)
            self.current_song = self.songs[self.songlist.curselection()[0]]

    def load_selected_songs(self, selected_songs):
        self.songs = selected_songs['Song ID'].tolist()
        self.songlist.delete(0, tk.END)
        for song in self.songs:
            self.songlist.insert("end", song)
        if self.songs:
            self.songlist.selection_set(0)
            self.current_song = self.songs[self.songlist.curselection()[0]]

    def play_music(self):
        if self.selected_songs is not None:
            self.play_selected_songs()
        else:
            if not self.paused:
                pygame.mixer.music.load(os.path.join(self.root.directory, self.current_song))
                pygame.mixer.music.play()
                self.start_time = time.time()
            else:
                pygame.mixer.music.unpause()
                self.paused = False
            self.update_timer()

    def pause_music(self):
        pygame.mixer.music.pause()
        self.paused = True

    def next_music(self):
        try:
            self.songlist.selection_clear(0, tk.END)
            self.songlist.selection_set(self.songs.index(self.current_song) + 1)
            self.current_song = self.songs[self.songlist.curselection()[0]]
            self.play_music()
        except:
            pass

    def prev_music(self):
        try:
            self.songlist.selection_clear(0, tk.END)
            self.songlist.selection_set(self.songs.index(self.current_song) - 1)
            self.current_song = self.songs[self.songlist.curselection()[0]]
            self.play_music()
        except:
            pass

    def set_volume(self, val):
        volume = float(val) / 100
        pygame.mixer.music.set_volume(volume)

    def update_timer(self):
        if pygame.mixer.music.get_busy():
            current_time = pygame.mixer.music.get_pos() // 1000
            mins, secs = divmod(current_time, 60)
            time_format = f"{mins:02}:{secs:02}"
            self.timer_label.config(text=time_format)
            self.root.after(1000, self.update_timer)
        else:
            self.timer_label.config(text="00:00")

    def update_visual_effect(self):
        if pygame.mixer.music.get_busy():
            self.canvas.delete("all")
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()
            num_bars = 30
            bar_width = width / num_bars
            for i in range(num_bars):
                bar_height = height * (0.5 + 0.5 * math.sin(i + time.time() - self.start_time))
                x0 = i * bar_width
                y0 = height - bar_height
                x1 = (i + 1) * bar_width
                y1 = height
                color = f'#{int(255 * (1 - bar_height / height)):02x}00{int(255 * (bar_height / height)):02x}'
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
            self.root.after(50, self.update_visual_effect)
        else:
            self.canvas.delete("all")

    def play_selected_songs(self):
        if self.current_song_index < len(self.selected_songs):
            song_path = os.path.join('/Users/jennyafren/PycharmProjects/ElectricalEngineeringProject/MusicFiles',
                                     self.selected_songs.iloc[self.current_song_index]['Song ID'])
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play()
            self.current_song_index += 1
            self.root.after(1000, self.check_if_song_finished)
        else:
            self.current_song_index = 0

    def check_if_song_finished(self):
        if not pygame.mixer.music.get_busy():
            self.play_selected_songs()
        else:
            self.root.after(1000, self.check_if_song_finished)


# Algorithm to select songs based on user input
def select_songs():
    # Load the Excel file
    file_path = '/Users/jennyafren/PycharmProjects/EngineeringProject2024Tau/single_bpm_songs_data.xlsx'
    df = pd.read_excel(file_path)
    # # Ensure 'BPM' column is converted to integer
    # df['BPM'] = pd.to_numeric(df['BPM'], errors='coerce').fillna(0).astype(int)

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
        return None

    max_intensity = intensity_options[training]
    print(f"How intense do you want the training to be? (from 1-{max_intensity})")
    intense = int(input().strip())

    if not (1 <= intense <= max_intensity):
        print("Invalid intensity level provided.")
        return None

    print("How long will you train? (in minutes)")
    duration = int(input().strip())

    print("Choose your BPM preference:")
    for key, value in bpm_preferences.items():
        print(f"{key}: {value.capitalize()}")

    bpm_preference_choice = int(input("Enter the number corresponding to your BPM preference: ").strip())
    bpm_preference = bpm_preferences.get(bpm_preference_choice, None)

    if bpm_preference is None:
        print("Invalid BPM preference provided.")
        return None

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
    filtered_songs = df[(df['BPM'].str.strip('[]').astype(float) >= bpm_range[0]) & (df['BPM'].str.strip('[]').astype(float) <= bpm_range[1])]

    if filtered_songs.empty:
        print("No songs found in the specified BPM range: " + str(bpm_range))
        return None

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

        segment_songs = filtered_songs[(filtered_songs['BPM'].str.strip('[]').astype(float) >= min_bpm) & (filtered_songs['BPM'].str.strip('[]').astype(float) < max_bpm)]
        if not segment_songs.empty:
            song = segment_songs.sample(n=1).iloc[0]  # Select a random song from the segment
            total_duration += song['Duration (minutes)']
            selected_songs = pd.concat([selected_songs, song.to_frame().T], ignore_index=True)
            if total_duration >= duration:
                break

    # Select songs until the total duration is close to the input duration
    for _, song in filtered_songs.iterrows():
        if total_duration + song['Duration (minutes)'] > duration + 1:
            continue
        total_duration += song['Duration (minutes)']
        selected_songs = pd.concat([selected_songs, song.to_frame().T], ignore_index=True)
        if total_duration >= duration and total_duration - duration < 1:
            break

    if total_duration - duration >= 1:
        # If we exceed the desired duration by 1 minute, try to remove the last song added
        last_song_duration = selected_songs.iloc[-1]['Duration (minutes)']
        if total_duration - last_song_duration >= duration and total_duration - last_song_duration - duration < 1:
            total_duration -= last_song_duration
            selected_songs = selected_songs[:-1]

    # Ensure the selected songs cover the entire BPM range
    if bpm_preference == "increased":
        selected_songs = selected_songs.sort_values(by='BPM').reset_index(drop=True)
    elif bpm_preference == "decreased":
        selected_songs = selected_songs.sort_values(by='BPM', ascending=False).reset_index(drop=True)
    elif bpm_preference == "parabolic+":
        selected_songs = pd.concat([
            selected_songs.iloc[:len(selected_songs) // 2].sort_values(by='BPM'),
            selected_songs.iloc[len(selected_songs) // 2:].sort_values(by='BPM', ascending=False)
        ]).reset_index(drop=True)
    elif bpm_preference == "parabolic-":
        selected_songs = pd.concat([
            selected_songs.iloc[:len(selected_songs) // 2].sort_values(by='BPM', ascending=False),
            selected_songs.iloc[len(selected_songs) // 2:].sort_values(by='BPM')
        ]).reset_index(drop=True)
    elif bpm_preference == "shuffle":
        selected_songs = selected_songs.sample(frac=1).reset_index(drop=True)

    print("Selected Songs for Training:")
    print(selected_songs)
    print(f"Total Duration: {total_duration} minutes")

    return selected_songs


if __name__ == "__main__":
    # Running the algorithm to select songs
    selected_songs = select_songs()

    # Creating the player and loading the selected songs
    if selected_songs is not None and not selected_songs.empty:
        root = tk.Tk()
        player = MusicPlayer(root)
        player.selected_songs = selected_songs
        player.load_selected_songs(selected_songs)  # Load the selected songs into the player
        player.play_music()
        root.mainloop()
