import spotipy
import json
from spotipy.oauth2 import SpotifyOAuth

# Set your Spotify API credentials and scope
scope = "user-library-modify"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# Define the name of the JSON file
file_name = "new_songs_to_add.json"

def find_track_uri(song_name, artist_name):
    """Searches for a track and returns its URI."""
    try:
        query = f"track:{song_name} artist:{artist_name}"
        result = sp.search(q=query, type='track', limit=1)

        if result and result['tracks']['items']:
            track = result['tracks']['items'][0]
            print(f"Found URI for '{song_name}' by '{artist_name}'")
            return track['uri']
        else:
            print(f"Could not find a track for '{song_name}' by '{artist_name}'")
            return None
    except Exception as e:
        print(f"An error occurred while searching for '{song_name}': {e}")
        return None

try:
    with open(file_name, 'r') as f:
        songs = json.load(f)

    track_uris_to_add = []
    
    for song in songs:
        song_name = song.get('name')
        artist_name = song.get('artistName')
        
        if song_name and artist_name:
            uri = find_track_uri(song_name, artist_name)
            if uri:
                track_uris_to_add.append(uri)
        else:
            print("Skipping a song entry due to missing 'name' or 'artistName'.")

    if track_uris_to_add:
        # Define the batch size (Spotify's limit is 50)
        batch_size = 50
        
        # Process the list of URIs in batches
        for i in range(0, len(track_uris_to_add), batch_size):
            batch = track_uris_to_add[i:i + batch_size]
            sp.current_user_saved_tracks_add(tracks=batch)
            print(f"\nSuccessfully added a batch of {len(batch)} songs to your liked songs.")
            
        print(f"\nCompleted! All {len(track_uris_to_add)} songs have been processed.")
    else:
        print("\nNo songs were found to add.")

except FileNotFoundError:
    print(f"Error: The file '{file_name}' was not found.")
except json.JSONDecodeError:
    print(f"Error: The file '{file_name}' is not a valid JSON file.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
