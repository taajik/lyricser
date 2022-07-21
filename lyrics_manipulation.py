
import os

from song import Song
from utils import report


def create_lyrics_file(path, files, lyrics_path=""):
    """Generate a text containing lyrics of all the songs in a folder."""

    lyrics_file = lyrics_path.strip()
    if not lyrics_file or lyrics_file == "/":
        lyrics_file = path

    folder = path.split("/")[-2]
    lyrics_file += folder + " (Lyrics).txt"
    inner_folders = []
    lyrics = (f"\n┌─{'─'*len(folder)}─┐" +
              f"\n│ {folder} │ {len(files)}" +
              f"\n└─{'─'*len(folder)}─┘\n")

    if os.path.isfile(lyrics_file):
        report(False, " X Lyrics file already exists: " + folder)
    else:
        # Add the lyrics of every file in this folder to 'lyrics'.
        for file in files:
            file = path + file

            if os.path.isfile(file):
                lyrics += f"\n\n{'─'*120}\n\n  {file[len(path):-4]}\n\n\n"
                try:
                    lyrics += Song(file).lyrics
                except Exception as e:
                    print(e)
                lyrics += "\n"
            elif os.path.isdir(file):
                inner_folders.append(file + "/")

        lyrics += "\n\n" + "─"*120 + "\n"

        # Save the lyrics text in a file.
        with open(lyrics_file, "w", encoding="utf-8") as lyricstxt:
            lyricstxt.write(lyrics)
        report(True, " Lyrics file generated: " + folder)
        # print(lyrics)

    # Call the function again for folders inside this one.
    # Each folder will generate a separate lyrics text.
    for inner_path in inner_folders:
        create_lyrics_file(inner_path,
                           sorted(os.listdir(inner_path)),
                           lyrics_path)


def edit_lyrics(path, files):
    """Write the lyrics to a text file and then
    read back the edited version to the song and save it.
    """

    inner_folders = []

    for file in files:
        file = path + file

        if os.path.isfile(file):
            try:
                song = Song(file)
            except Exception as e:
                print(e)
                continue
            lyrics = song.lyrics

            # Write the lyrics in the editor file.
            with open("lyrics_editor.txt", "w", encoding="utf-8") as lyricstxt:
                lyricstxt.write(lyrics)

            # Wait until edits are confirmed.
            if input(file.split("/")[-1] + " >< "):
                break

            # Read the edited lyrics from the editor file.
            with open("lyrics_editor.txt", "r", encoding="utf-8") as lyricstxt:
                lyrics = lyricstxt.read().strip()

            # Add the new lyrics to the song and save it.
            song.lyrics = lyrics
            song.save()

        elif os.path.isdir(file):
            inner_folders.append(file + "/")

    # Call the function again for folders inside this one.
    for inner_path in inner_folders:
        edit_lyrics(inner_path, sorted(os.listdir(inner_path)))


def search_lyrics(path, files):
    """Search for a phrase in all of the lyrics files
    inside the entered folder.

    The results lists the song and file names that include the phrase.
    """

    q = input("Search phrase: ").lower()
    print()
    if len(q) < 4:
        print(" X It's too short (four characters minimum)")
        return

    for album in files:
        if album[-4:].lower() != ".txt":
            continue

        file = open(path + album, "r", encoding="utf-8")
        lyrics = file.read()
        # Divide the full lyrics file into separate song lyrics.
        lyrics = lyrics.split("─" * 120)[1:-1]

        for song in lyrics:
            if q in song.lower():
                # For each match, print the song and file name
                print(album, song.splitlines()[2])

        file.close()
