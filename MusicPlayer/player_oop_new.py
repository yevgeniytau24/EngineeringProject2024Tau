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
            file='/Users/jennyafren/PycharmProjects/EngineeringProject2024Tau/MusicPlayer/icons/nplay button_player_icon.png')
        self.pause_btn_img = PhotoImage(
            file='/Users/jennyafren/PycharmProjects/EngineeringProject2024Tau/MusicPlayer/icons/npause_player_icon.png')
        self.next_btn_img = PhotoImage(
            file='/Users/jennyafren/PycharmProjects/EngineeringProject2024Tau/MusicPlayer/icons/nnext_player_icon.png')
        self.prev_btn_img = PhotoImage(
            file='/Users/jennyafren/PycharmProjects/EngineeringProject2024Tau/MusicPlayer/icons/nprevious_icon.png')

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
        self.root.directory = "/path/to/mp3music_files"

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
        self.selected_songs = selected_songs
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
            song_path = os.path.join('/Users/jennyafren/PycharmProjects/EngineeringProject2024Tau/mp3music_files',
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