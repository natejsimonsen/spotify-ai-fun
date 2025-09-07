import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "playlist-read-private playlist-read-collaborative"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

playlists_list = []
results = sp.current_user_playlists()
playlists_list.extend(results['items'])

# Paginate through the results to get all playlists
while results['next']:
    results = sp.next(results)
    playlists_list.extend(results['items'])

# Now, playlists_list contains all the user's playlists
for playlist in playlists_list:
    print(f"Name: {playlist['name']}, URI: {playlist['uri']}")
