from tkinter import filedialog
from tkinter import *
import pygame
import os
import math
import time

root = Tk()
root.title("Music Player")
root.geometry("400x700")

pygame.mixer.init()
menubar = Menu(root)
root.config(menu=menubar)

songs = []
current_song = ""
paused = False
start_time = time.time()

def load_music():
    global current_song
    root.directory = "/Users/jennyafren/PycharmProjects/ElectricalEngineeringProject/MusicFiles"

    if not os.path.isdir(root.directory):
        root.directory = filedialog.askdirectory()

    for song in os.listdir(root.directory):
        name, ext = os.path.splitext(song)
        if ext == ".mp3":
            songs.append(song)
    for song in songs:
        songlist.insert("end", song)

    if songs:
        songlist.selection_set(0)
        current_song = songs[songlist.curselection()[0]]

def play_music():
    global current_song, paused, start_time

    if not paused:
        pygame.mixer.music.load(os.path.join(root.directory, current_song))
        pygame.mixer.music.play()
        start_time = time.time()
    else:
        pygame.mixer.music.unpause()
        paused = False
    update_timer()
    update_visual_effect()

def pause_music():
    global paused
    pygame.mixer.music.pause()
    paused = True

def next_music():
    global current_song, paused
    try:
        songlist.selection_clear(0, END)
        songlist.selection_set(songs.index(current_song) + 1)
        current_song = songs[songlist.curselection()[0]]
        play_music()
    except:
        pass

def prev_music():
    global current_song, paused
    try:
        songlist.selection_clear(0, END)
        songlist.selection_set(songs.index(current_song) - 1)
        current_song = songs[songlist.curselection()[0]]
        play_music()
    except:
        pass

def set_volume(val):
    volume = float(val) / 100
    pygame.mixer.music.set_volume(volume)

def update_timer():
    if pygame.mixer.music.get_busy():
        current_time = pygame.mixer.music.get_pos() // 1000
        mins, secs = divmod(current_time, 60)
        time_format = f"{mins:02}:{secs:02}"
        timer_label.config(text=time_format)
        root.after(1000, update_timer)
    else:
        timer_label.config(text="00:00")

def update_visual_effect():
    if pygame.mixer.music.get_busy():
        canvas.delete("all")
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        num_bars = 30
        bar_width = width / num_bars
        for i in range(num_bars):
            bar_height = height * (0.5 + 0.5 * math.sin(i + time.time() - start_time))
            x0 = i * bar_width
            y0 = height - bar_height
            x1 = (i + 1) * bar_width
            y1 = height
            color = f'#{int(255 * (1 - bar_height / height)):02x}00{int(255 * (bar_height / height)):02x}'
            canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
        root.after(50, update_visual_effect)
    else:
        canvas.delete("all")

organise_menu = Menu(menubar, tearoff=False)
organise_menu.add_command(label='Select Folder', command=load_music)
menubar.add_cascade(label='Organize', menu=organise_menu)

songlist = Listbox(root, bg="black", fg="lime", font=("Helvetica", 16), width=100, height=15)
songlist.pack()

play_btn_img = PhotoImage(file='/Users/jennyafren/PycharmProjects/ElectricalEngineeringProject/nplay button_player_icon.png')
pause_btn_img = PhotoImage(file='/Users/jennyafren/PycharmProjects/ElectricalEngineeringProject/npause_player_icon.png')
next_btn_img = PhotoImage(file='/Users/jennyafren/PycharmProjects/ElectricalEngineeringProject/nnext_player_icon.png')
prev_btn_img = PhotoImage(file='/Users/jennyafren/PycharmProjects/ElectricalEngineeringProject/nprevious_icon.png')

control_frame = Frame(root)
control_frame.pack()

play_btn = Button(control_frame, image=play_btn_img, borderwidth=0, command=play_music)
pause_btn = Button(control_frame, image=pause_btn_img, borderwidth=0, command=pause_music)
next_btn = Button(control_frame, image=next_btn_img, borderwidth=0, command=next_music)
prev_btn = Button(control_frame, image=prev_btn_img, borderwidth=0, command=prev_music)

play_btn.grid(row=0, column=2, padx=7, pady=10)
pause_btn.grid(row=0, column=1, padx=7, pady=10)
next_btn.grid(row=0, column=3, padx=7, pady=10)
prev_btn.grid(row=0, column=0, padx=7, pady=10)

# Add volume slider
volume_frame = Frame(root)
volume_frame.pack(pady=10)

volume_label = Label(volume_frame, text="Volume")
volume_label.pack(side=LEFT)

volume_slider = Scale(volume_frame, from_=0, to_=100, orient=HORIZONTAL, command=set_volume)
volume_slider.set(50)  # Set default volume to 50%
volume_slider.pack(side=LEFT)

# Add timer label
timer_label = Label(root, text="00:00", font=("Helvetica", 16), bg="black", fg="lime")
timer_label.pack(pady=10)

# Add canvas for visual effect
canvas = Canvas(root, bg="black", width=400, height=200)
canvas.pack(pady=10)

# Automatically load music from the specified folder
load_music()

root.mainloop()
