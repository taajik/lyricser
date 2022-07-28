
import os
import re

from lyricsgenius import Genius

from song import Song
from utils import report


# genius = Genius(excluded_terms=["(Live)", "(Remix)"])
genius = Genius()


def get_lyrics(title, artist):
    """Searche for lyrics on Genius."""

    # lyrics = ""
    # lyrics = genius.lyrics( input(title + " - " + artist + "\n  url: ") )        # search by supplying the song url
    # lyrics = genius.search_song(song_id= input("  id: "), get_full_info=False).lyrics        # search by supplying the song id
    lyrics = genius.search_song(title, artist, get_full_info=False).lyrics        # search by reading song tags

    # Format the lyrics
    lyrics = re.sub("\n*\[", "\n\n[", lyrics)
    lyrics = re.sub("^.*\n", "", lyrics)
    lyrics = lyrics.replace("’", "'").strip()
    lyrics = re.sub("\d*Embed$", "", lyrics)

    return lyrics


def set_lyrics(file):
    """Find and set the lyrics of a song according to its title and artist."""

    # Load the mp3 file's tags.
    try:
        song = Song(file)
    except Exception as e:
        report(False, e)
        return

    t = song.title
    aa = song.album_artist

    # Check for existence and ambiguity of title and artist,
    # and get it directly from input if invalid.
    # Empty input means use it as is.
    if not t or re.search("[\(\)\.\-’]", t):
        print("X Invalid title:", t)
        t = input("  title: ")
        if not t.strip():
            t = song.title
    if not aa:
        print("X Invalid artist:", aa)
        aa = input("  artist: ")
        if not aa.strip():
            aa = song.album_artist

    # Set the lyrics and save the file.
    try:
        lyrics = get_lyrics(t, aa)
        song.lyrics = lyrics
        song.save()
        report(True)
    except Exception:
        report(False, " X Lyrics Error: " + file)


def auto_add_lyrics(path, files):
    """Loop through the songs in one folder and add lyrics to them."""

    print("\n" + "─"*len(path) + "──┐")
    print(" " + path + " │", len(files))
    print("─"*len(path) + "──┘")
    inner_folders = []

    i = 0
    for file in files:
        file = path + file

        if os.path.isfile(file):
            i += 1
            print("\n", i, end=": ")
            set_lyrics(file)

        # if 'file' is a folder, store it to call the function on it later.
        elif os.path.isdir(file):
            inner_folders.append(file + "/")

    # Call the function again for folders inside this one.
    for inner_path in inner_folders:
        auto_add_lyrics(inner_path, sorted(os.listdir(inner_path)))
