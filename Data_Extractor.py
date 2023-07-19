import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

def get_track_genres(track_id):
    track = sp.track(track_id)
    artists = track['artists']
    genres = []
    for artist in artists:
        artist_id = artist['id']
        artist = sp.artist(artist_id)
        genres += artist['genres']
    return genres

# Replace with your Spotify API credentials
client_id = '4b069831c6284a0ea2a917be7d8ce34f'
client_secret = 'c9767a23e8d44d698f3cae54e500a336'

# Authenticate with the Spotify Web API
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Replace with the ID of the playlist you want to extract data from
playlist_id = '4O7sEu8DEkAdGysFhfvzqz'

# Get the playlist's metadata
playlist = sp.playlist(playlist_id)

# Get the playlist's tracks
tracks = sp.playlist_tracks(playlist_id)

# Create an empty list to store the data for each track
data = []
# Loop through each page of tracks
while tracks:
    # Loop through each track on the current page
    for item in tracks['items']:
        track = item['track']
        track_name = track['name']
        album_name = track['album']['name']
        artist_name = track['artists'][0]['name']
        release_date = track['album']['release_date']
        length = track['duration_ms'] / 1000.0
        popularity = track['popularity']
        audio_features = sp.audio_features(track['id'])[0]
        acousticness = audio_features['acousticness']
        danceability = audio_features['danceability']
        energy = audio_features['energy']
        instrumentalness = audio_features['instrumentalness']
        liveness = audio_features['liveness']
        loudness = audio_features['loudness']
        speechiness = audio_features['speechiness']
        tempo = audio_features['tempo']
        time_signature = audio_features['time_signature']
        genres = get_track_genres(track['id'])

# Append the data for the current track to the list
        data.append([track_name, album_name, artist_name, release_date, length, popularity, acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, tempo, time_signature, genres])

# Check if there are more pages of tracks
    tracks = sp.next(tracks)
    
# Create a new DataFrame with the data
columns = ['name', 'album', 'artist', 'release_date', 'length', 'popularity', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'time_signature', 'genres']
df = pd.DataFrame(data, columns=columns)
df.to_csv("Spotify_Data_Extraction.csv", sep = ',')
