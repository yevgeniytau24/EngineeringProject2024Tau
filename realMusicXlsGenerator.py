import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# Spotify API credentials
client_id = 'YOUR_SPOTIFY_CLIENT_ID'
client_secret = 'YOUR_SPOTIFY_CLIENT_SECRET'

# Authenticate with the Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

def get_songs_by_artist(artist_name, limit=50):
    results = sp.search(q=f'artist:{artist_name}', type='track', limit=limit)
    tracks = results['tracks']['items']
    song_data = []
    for track in tracks:
        song_id = track['id']
        song_name = track['name']
        album_name = track['album']['name']
        release_date = track['album']['release_date']
        duration_ms = track['duration_ms']
        duration_s = duration_ms // 1000
        bpm = sp.audio_features([song_id])[0]['tempo']
        song_data.append({
            "Song Name": song_name,
            "Album Name": album_name,
            "Release Date": release_date,
            "Total Duration (minutes)": duration_s / 60,
            "Total Duration (seconds)": duration_s,
            "Total Duration (mm:ss)": format_seconds_to_mm_ss(duration_s),
            "BPM": bpm
        })
    return song_data

def format_seconds_to_mm_ss(seconds):
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{int(minutes):02}:{int(remaining_seconds):02}"

def save_to_excel(song_data, filename):
    df = pd.DataFrame(song_data)
    df.to_excel(filename, index=False)

# Fetch songs by Taylor Swift
artist_name = 'Taylor Swift'
song_data = get_songs_by_artist(artist_name, limit=150)

# Save the data to an Excel file
filename = f"{artist_name.replace(' ', '_')}_songs_data.xlsx"
save_to_excel(song_data, filename)

print(f"Song data for {artist_name} generated and saved to {filename}")
