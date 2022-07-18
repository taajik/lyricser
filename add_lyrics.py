
import os
import re

import eyed3
from lyricsgenius import Genius
from mutagen.mp4 import MP4

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
    lyrics = lyrics.replace("’", "'").strip()
    lyrics = re.sub("[0-9]*EmbedShare URLCopyEmbedCopy$", "", lyrics)

    return lyrics


def set_lyrics_mp3(file):
    """Find and set the lyrics of an mp3 song
    according to its title and artist.
    """

    # Load the mp3 file's tags.
    try:
        tag = eyed3.load(file).tag
    except Exception:
        report(False, " X File Error: " + file)
        return

    t = tag.title
    aa = tag.album_artist

    # If the title is ambiguous, get it directly from input.
    if re.match("^[^\(\)\.\-’]+$", t):
        print(t, "-", aa)
        t = input("  t: ")
        # Just an enter means use it as is.
        if not t.strip():
            t = tag.title

    # Set the lyrics and save the file.
    try:
        lyrics = get_lyrics(t, aa)
        tag.lyrics.set(lyrics)
        tag.save(version=eyed3.id3.ID3_V2_4, encoding="utf8")
        report(True)
    except Exception:
        report(False, " X Lyrics Error: " + file)


def set_lyrics_m4a(file):
    """Find and set the lyrics of an m4a song
    according to its title and artist.
    """

    # Load the m4a file's tags.
    try:
        tag = MP4(file).tags
        t = tag.get("\xa9nam")
        aa = tag.get("aART")
    except Exception:
        report(False, " X File Error: " + file)

    # There could be more than one title or artist found in the tags.
    # In that case, they need to be entered manually.
    if len(t) == 1 and len(aa) == 1:
        t = t[0]
        aa = aa[0]
    else:
        print(t, "-", aa)
        t = input("  t: ")
        aa = input("  aa: ")

    # If the title is ambiguous, get it directly from input.
    if re.match("^[^\(\)\.\-’]+$", t):
        print(t, "-", aa)
        t = input("  t: ")
        # Just an enter means use it as is.
        if not t.strip():
            t = tag.get("\xa9nam")[0]

    try:
        # Set the lyrics and save the file.
        lyrics = get_lyrics(t, aa)
        tag["\xa9lyr"] = lyrics
        tag.save(file)
        report(True)
    except Exception:
        report(False, " X Lyrics Error: " + file)


def set_lyrics(path, files):
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

            if file[-4:].lower() == ".mp3":
                set_lyrics_mp3(file)
            elif file[-4:].lower() == ".m4a":
                set_lyrics_m4a(file)
            else:
                report(False, " X Not supported file format: " + file)

        # if 'file' is a folder, store it to call the function on it later.
        elif os.path.isdir(file):
            inner_folders.append(file + "/")

    # Call the function recursively for the folders inside this one.
    for inner_path in inner_folders:
        set_lyrics(inner_path, sorted(os.listdir(inner_path)))
