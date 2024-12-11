import tkinter as tk
from tkinter import filedialog, ttk
import pygame
import os

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("400x350")

        pygame.mixer.init()

        self.current_song = ""
        self.paused = False

        self.add_widgets()

    def add_widgets(self):
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=10)

        self.load_button = ttk.Button(self.root, text="Load Song", command=self.load_song)
        self.load_button.pack(pady=10)

        self.play_button = ttk.Button(self.root, text="Play", command=self.play_song)
        self.play_button.pack(pady=10)

        self.pause_button = ttk.Button(self.root, text="Pause/Resume", command=self.pause_song)
        self.pause_button.pack(pady=10)

        self.stop_button = ttk.Button(self.root, text="Stop", command=self.stop_song)
        self.stop_button.pack(pady=10)

        self.volume_slider = ttk.Scale(self.root, from_=0, to_=1, orient="horizontal", command=self.set_volume)
        self.volume_slider.set(0.05)  # Set default volume to 50%
        self.volume_slider.pack(pady=10)

        self.volume_label = ttk.Label(self.root, text="Volume")
        self.volume_label.pack()

    def load_song(self):
        self.current_song = filedialog.askopenfilename(filetypes=(("MP3 Files", "*.mp3"),))
        if self.current_song:
            pygame.mixer.music.load(self.current_song)

    def play_song(self):
        if self.current_song:
            pygame.mixer.music.play()

    def pause_song(self):
        if self.paused:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
        self.paused = not self.paused

    def stop_song(self):
        pygame.mixer.music.stop()

    def set_volume(self, val):
        volume = float(val)
        pygame.mixer.music.set_volume(volume)

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()
