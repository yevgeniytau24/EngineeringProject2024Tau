import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib.colors as mcolors

# Create a custom colormap
colors = [(2.5, 2, 3), (7, 2, 2), (6.5, 7, 15)]  # Dark blue to light blue
n_bins = 500  # Discretizes the interpolation into bins
cmap_name = 'custom_blue'
custom_cmap = mcolors.LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)



# Load the audio file
file_path = '/Users/jennyafren/PycharmProjects/EngineeringProject2024Tau/mp3music_files/alarm.wav'
if os.path.exists(file_path):
    print("File exists.")
else:
    print("File does not exist.")

y, sr = librosa.load(file_path)
# Estimate the tempo (BPM)
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
tempo = tempo[0]
print(f"Estimated tempo: {tempo:.2f} BPM")
beat_times = librosa.frames_to_time(beat_frames, sr=sr)

print(f"Audio duration: {len(y) / sr:.2f} seconds")
# Compute the Short-Time Fourier Transform (STFT)
D = np.abs(librosa.stft(y))
print(f"STFT shape: {D.shape}")
# Convert the amplitude spectrogram to dB-scaled spectrogram
S_db = librosa.amplitude_to_db(D, ref=np.max)
# Plot the spectrogram
plt.figure(figsize=(25, 15))
librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='log')
plt.colorbar(format='%+2.0f dB')
# Plot the spectrogram with the custom colormap
plt.figure(figsize=(25, 15))
librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='log', cmap=custom_cmap)
plt.colorbar(format='%+2.0f dB')
plt.title('Spectrogram')
plt.show()

plt.show()
