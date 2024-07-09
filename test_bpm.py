import librosa
import librosa.display
import matplotlib.pyplot as plt

# Load the audio file
import numpy as np

file_path1 = f"/Users/jennyafren/PycharmProjects/ElectricalEngineeringProject/MusicFiles/alarm.wav"
file_path2 = f"/Users/jennyafren/PycharmProjects/ElectricalEngineeringProject/MusicFiles/alarm2.wav"
file_path3 = f"/Users/jennyafren/PycharmProjects/ElectricalEngineeringProject/MusicFiles/violin.wav"
file_path4 = f"/Users/jennyafren/PycharmProjects/ElectricalEngineeringProject/MusicFiles/testfile3.wav"
file_path5 = f"/User s/jennyafren/PycharmProjects/ElectricalEngineeringProject/MusicFiles/testfile2.wav"
file_path6 = f"/Users/jennyafren/PycharmProjects/ElectricalEngineeringProject/MusicFiles/electronic.wav"


list_of_files = [file_path1, file_path2, file_path3, file_path4, file_path5, file_path6]
for file in list_of_files:
    y, sr = librosa.load(file)

    # Estimate the tempo (BPM)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

    # Ensure tempo is a single value
    if isinstance(tempo, np.ndarray):
        tempo = tempo[0]

    print(f"Estimated tempo: {tempo:.2f} BPM")

    # Convert the beat frames to time
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    print(f"Audio duration: {len(y) / sr:.2f} seconds")
    # Compute the Short-Time Fourier Transform (STFT)
    D = np.abs(librosa.stft(y))
    print(f"STFT shape: {D.shape}")
    # Convert the amplitude spectrogram to dB-scaled spectrogram
    S_db = librosa.amplitude_to_db(D, ref=np.max)
    # Plot the waveform with beat markers
    plt.figure(figsize=(10, 6))
    librosa.display.waveshow(y, sr=sr, alpha=0.6)
    # librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='log')
    plt.vlines(beat_times, -1, 1, color='g', alpha=0.9, linestyle='--', label='Beats')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude of ' + file)
    plt.title('Waveform with Beat Markers')
    plt.legend()
    plt.show()
