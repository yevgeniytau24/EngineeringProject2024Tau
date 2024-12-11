import pandas as pd
print("What kind of training are you planning to do?")
training = input()
print("How long will you train?")
duration = input()
# Read the Excel file
df = pd.read_excel('single_bpm_songs_data.xlsx')
song_bpm = df['BPM']
song_id = df['Song ID']
if training == "running":
    filtered_songs = df[(df['BPM'] >= 120) & (df['BPM'] <= 200)]
    song_ids_with_bpm_120_to_200 = filtered_songs['Song ID'].tolist()
    print(song_ids_with_bpm_120_to_200)
if training == "walking":
    filtered_songs = df[(df['BPM'] >= 90) & (df['BPM'] <= 110)]
    song_ids_with_bpm_90_to_110 = filtered_songs['Song ID'].tolist()
    print(song_ids_with_bpm_90_to_110)
if training == "yoga":
    filtered_songs = df[(df['BPM'] >= 50) & (df['BPM'] <= 140)]
    song_ids_with_bpm_50_to_140 = filtered_songs['Song ID'].tolist()
    print(song_ids_with_bpm_50_to_140)
if training == "gym":
    filtered_songs = df[(df['BPM'] >= 100) & (df['BPM'] <= 180)]
if training == "walking1":
    filtered_songs = df.loc[(df['BPM'] >= 90) & (df['BPM'] <= 110)]
    sum = filtered_songs['Total Duration (minutes)'].sum()
    print(sum)
    while sum > int(duration):
        filtered_songs = filtered_songs.iloc[:-1,:]
        filtered_songs= filtered_songs.sample(frac=1)
        sum = filtered_songs['Total Duration (minutes)'].sum()
    print(filtered_songs.sample(frac=1))
    #
    #     song_ids_with_bpm_90_to_110 = filtered_songs['Song ID'].tolist()
    #     print(song_ids_with_bpm_90_to_110)
    # song_ids_with_bpm_100_to_180 = []
    # #print(song_ids_with_bpm_50_to_140)
    # cumulative_duration = 0
    # songs_list = []
    # for index, row in filtered_songs.iterrows():
    #     song_duration = row['Total Duration (minutes)']
    #     if cumulative_duration + song_duration > duration:
    #         break
    #     # Add the song ID to the list
    #     song_ids_with_bpm_100_to_180.append(row['Song ID'])
    #     # Update the cumulative duration
    #     cumulative_duration += song_duration
    #     # Print the list
    #     print(song_ids_with_bpm_100_to_180)
    #
    #
