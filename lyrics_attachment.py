
import re

from song import Song
from utils import report, get_header


def format_lyrics(lyrics: str):
    """Format the lyrics from the Genius for adding them to songs."""

    lyrics = lyrics.replace("[?]", "")
    lyrics = re.sub("\n*\[", "\n\n[", lyrics)
    lyrics = re.sub("^.*\n", "", lyrics)
    lyrics = lyrics.replace("’", "'").replace(" ", " ").strip()
    lyrics = re.sub("\d*Embed$", "", lyrics)

    return lyrics


def get_song_lyrics(t, aa, genius):
    """Search for lyrics of a song in Genius
    according to its title and artist.
    """

    if t is None:
        print("X Title not found.")
        t = input("  title: ")
    else:
        t = re.sub(" \(.*\)", "", t)
    if aa is None:
        print("X Artist not found.")
        aa = input("  artist: ")

    try:
        # lyrics = genius.lyrics( input(t + " - " + aa + "\n  url: ") )
        lyrics = genius.search_song(t, aa, get_full_info=False).lyrics
    except KeyboardInterrupt:
        raise SystemExit

    return lyrics


def auto_add_lyrics(path, genius, is_album=False):
    """Loop through the songs in one folder and add lyrics to them."""

    print(get_header(path))
    inner_folders = []

    if is_album:
        folder = path.name.split(" - ")
        if len(folder) == 2:
            folder.reverse()
            try:
                album = genius.search_album(*folder, get_full_info=False)
            except KeyboardInterrupt:
                raise SystemExit

    i = 0
    for file in sorted(path.iterdir()):
        if file.is_file():
            i += 1
            print("\n" + str(i).rjust(3), end=". ")

            try:
                song = Song(file)
            except Exception as e:
                report(False, e)
                return
            t = song.title
            aa = song.album_artist

            # Get the lyrics of this song.
            if is_album:
                try:
                    lyrics = album.songs[i-1].lyrics
                    print(f'"{t}" by {aa}')
                except Exception:
                    lyrics = ""
            else:
                lyrics = get_song_lyrics(t, aa, genius)
            lyrics = format_lyrics(lyrics)

            # Set the lyrics and save the file.
            try:
                song.lyrics = lyrics
                song.save()
                report(True)
                if is_album:
                    print("Done.")
            except Exception:
                report(False, " X Lyrics Error: " + file.name)

        # if 'file' is a folder, store it to call the function on it later.
        elif file.is_dir():
            inner_folders.append(file)
    print()

    # Call the function again for folders inside this one.
    for inner_path in inner_folders:
        auto_add_lyrics(inner_path, genius, is_album)
