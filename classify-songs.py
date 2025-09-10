import json
import os
import sys
from os import listdir
from os.path import isfile, join

import spotipy
from colorama import Fore, init
from spotipy.oauth2 import SpotifyOAuth

from music_ai import get_genre
from utils import clear_terminal

# Set your Spotify API credentials and scope
scope = "user-library-modify playlist-read-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

init(autoreset=True)


def get_playlist_tracks(playlist_id):
    """
    Retrieves all tracks from a given playlist.
    """
    tracks = []
    results = sp.playlist_items(playlist_id)
    tracks.extend(results["items"])
    while results["next"]:
        results = sp.next(results)
        tracks.extend(results["items"])
    return tracks


def save_all_songs():
    """
    Main function to get all playlist tracks and save them to JSON files.
    """
    os.makedirs("playlists", exist_ok=True)

    playlists = sp.current_user_playlists()

    for playlist in playlists["items"]:
        playlist_name = playlist["name"]
        playlist_id = playlist["id"]
        print(f"Processing playlist: {playlist_name}")

        all_tracks = []
        try:
            tracks_info = get_playlist_tracks(playlist_id)
            for item in tracks_info:
                track = item["track"]
                if track and track["name"] and track["album"] and track["artists"]:
                    track_data = {
                        "name": track["name"],
                        "albumName": track["album"]["name"],
                        "artistName": track["artists"][0]["name"],
                    }
                    all_tracks.append(track_data)
            filename = (
                f"playlists/{playlist_name.replace('/', '_').replace(':', '_')}.json"
            )
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(all_tracks, f, ensure_ascii=False, indent=4)
            print(
                f"Saved {len(all_tracks)} tracks from '{playlist_name}' to {filename}"
            )

        except Exception as e:
            print(f"An error occurred while processing playlist '{playlist_name}': {e}")


def get_playlist_file_data():
    playlist_data = {}
    path = "playlists"
    playlists = [f for f in listdir(path) if isfile(join(path, f))]
    for playlist in playlists:
        try:
            with open(join(path, playlist), "r") as playlist_file:
                playlist_key = playlist.split(".")[0]
                playlist_data[playlist_key] = json.load(playlist_file)
        except Exception as e:
            print(f"Could not open file: {e}")
    return playlist_data


def add_genres_to_playlist(genres):
    """
    Returns a list of genres that a user specifies
    Genre must be in the accepted-genres.json file
    """
    user_input = ""
    genres_to_add = []
    accepted_genres = []

    try:
        with open("accepted-genres.json", "r") as json_data:
            accepted_genres = json.load(json_data)
    except Exception as e:
        print(f"Could not open accepted-genres.json file: {e}")

    while True:
        print(Fore.MAGENTA + "(Add Genre) Current Genres:")
        [print(Fore.GREEN + "  " + g) for g in genres]
        [print(Fore.GREEN + "  " + g) for g in genres_to_add]
        print()
        user_input = input("Add genre (q to quit): " + Fore.WHITE)
        if user_input.lower().strip() == "q":
            break

        genre = user_input.strip().title()
        if genre not in accepted_genres:
            print(Fore.RED + "Genre not accepted, only acceptable genres are: ")
            for g in accepted_genres:
                print("    " + g)
            continue
        genres_to_add.append(genre)
        clear_terminal()
    return genres_to_add


def remove_genres(genres):
    """
    Lets a user "delete" genres by returning a new list without those genres
    """
    user_input = ""
    genres_to_delete = []

    while user_input.lower().strip() != "q":
        print(Fore.MAGENTA + "(Remove Genre) Current Genres:")
        [print(Fore.GREEN + "  " + g) for g in genres if g not in genres_to_delete]
        print()
        user_input = input("Remove genre (q to quit): ")
        genre = user_input.strip().title()
        if genre not in genres:
            clear_terminal()
            print(Fore.RED + "Genre not accepted, only genres left are: ")
            for g in genres:
                print("    " + g)
            continue
        genres_to_delete.append(genre)
        clear_terminal()

    new_genres = [genre for genre in genres if genre not in genres_to_delete]

    return new_genres


def prompt_for_continue(playlist, genre):
    clear_terminal()
    print(Fore.MAGENTA + "(Save) Current Genres:")
    for g in genre["genres"]:
        print("    " + Fore.GREEN + g)
    print()

    user_input = input(f"Save genres for {playlist}? (y/n/a/d): ")

    return user_input.lower().strip()


def save_playlist_genre(playlist, genre):
    """Saves the playlist genres genres/{playlist}.json, with prompts to add / remove genres"""
    os.makedirs("genres", exist_ok=True)
    user_input = ""
    save = True

    while user_input != "y":
        user_input = prompt_for_continue(playlist, genre)
        if user_input == "n":
            save = False
            break

        if user_input == "a":
            clear_terminal()
            genre["genres"].extend(add_genres_to_playlist(genre["genres"]))

        if user_input == "d":
            clear_terminal()
            genre["genres"] = remove_genres(genre["genres"])

    if not save:
        return

    try:
        with open(f"genres/{playlist}.json", "w") as playlist_file:
            json.dump(genre, playlist_file, indent=4)
    except Exception as e:
        print(f"Cannot save playlist genre file at genres/{playlist}.json: {e}")


if __name__ == "__main__":
    try:
        # save_all_songs()
        playlists = get_playlist_file_data()
        for playlist_key in playlists:
            genre = get_genre(playlist_key)
            save_playlist_genre(playlist_key, genre)

        clear_terminal()
    except KeyboardInterrupt:
        sys.exit(0)
