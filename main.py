import json

with open('pandora-tracks.json', 'r') as file:
    pandora_data = json.load(file)['tracks']

with open('spotify-tracks.json', 'r') as file:
    spotify_data = json.load(file)['tracks']

def remove_duplicates(tracks):
    new_tracks = []
    for track in tracks:
        if track not in new_tracks:
            new_tracks.append(track)
    return new_tracks

def in_spotify_tracks(track, spotify_tracks):
    for spotify_track in spotify_tracks:
        if track['name'].lower() == spotify_track['name'].lower():
            return True
    return False

def get_new_tracks_from_pandora(pandora_tracks, spotify_tracks):
    new_tracks = []
    for track in pandora_tracks:
        in_spotify = in_spotify_tracks(track, spotify_tracks)
        if not in_spotify:
            new_tracks.append(track)
    return new_tracks

if __name__ == "__main__":
    pandora_tracks = remove_duplicates(pandora_data)
    spotify_tracks = spotify_data

    new_tracks_to_add = get_new_tracks_from_pandora(pandora_tracks, spotify_tracks)
    with open('new_songs_to_add.json', 'w') as f:
        json.dump(new_tracks_to_add, f, indent=4)
