import spotipy
import json
import os
from spotipy.oauth2 import SpotifyOAuth

# Set your Spotify API credentials and scope
scope = "user-library-modify playlist-read-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

def get_playlist_tracks(playlist_id):
    """
    Retrieves all tracks from a given playlist.
    """
    tracks = []
    results = sp.playlist_items(playlist_id)
    tracks.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

def save_all_songs():
    """
    Main function to get all playlist tracks and save them to JSON files.
    """
    # Create the 'playlists' directory if it doesn't exist
    if not os.path.exists('playlists'):
        os.makedirs('playlists')

    # Get the current user's playlists
    playlists = sp.current_user_playlists()

    # Iterate through each playlist
    for playlist in playlists['items']:
        playlist_name = playlist['name']
        playlist_id = playlist['id']
        print(f"Processing playlist: {playlist_name}")

        all_tracks = []
        try:
            tracks_info = get_playlist_tracks(playlist_id)
            for item in tracks_info:
                track = item['track']
                if track and track['name'] and track['album'] and track['artists']:
                    track_data = {
                        "name": track['name'],
                        "albumName": track['album']['name'],
                        "artistName": track['artists'][0]['name']
                    }
                    all_tracks.append(track_data)
            
            # Save the tracks to a JSON file
            # Use a sanitized playlist name for the filename
            filename = f"playlists/{playlist_name.replace('/', '_').replace(':', '_')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(all_tracks, f, ensure_ascii=False, indent=4)
            print(f"Saved {len(all_tracks)} tracks from '{playlist_name}' to {filename}")

        except Exception as e:
            print(f"An error occurred while processing playlist '{playlist_name}': {e}")

if __name__ == "__main__":
    save_all_songs()
