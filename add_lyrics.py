
import os
import re

import eyed3
from mutagen.mp4 import MP4
from lyricsgenius import Genius

from search_lyrics import search_lyrics


# number of
added_lyrics = 0
not_added_lyrics = 0

def added(is_successful):
    """Count the number of successful and
    unsuccessful lyrics attachments.
    """

    global added_lyrics, not_added_lyrics
    if is_successful:
        added_lyrics += 1
    else:
        not_added_lyrics += 1


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
        print(" X File Error:", file)
        added(False)
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
        added(True)
    except Exception:
        print(" X Lyrics Error:", file)
        added(False)


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
        print(" X File Error:", file)
        added(False)

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
        added(True)
    except Exception:
        print(" X Lyrics Error:", file)
        added(False)


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
                print(" X Not supported file format:", file)
                added(False)

        # if 'file' is a folder, store it to call the function on it later.
        elif os.path.isdir(file):
            inner_folders.append(file + "/")

    # Call the function recursively for the folders inside this one.
    for inner_path in inner_folders:
        set_lyrics(inner_path, sorted(os.listdir(inner_path)))


def load_lyrics(file):
    """Return the lyrics of a song."""

    try:
        if file[-4:].lower() == ".mp3":
            lyrics = eyed3.load(file).tag.lyrics[0].text
        elif file[-4:].lower() == ".m4a":
            lyrics = MP4(file).tags.get("\xa9lyr")[0]
        else:
            lyrics = " X Not supported file format"
    except Exception:
        lyrics = " X No Lyrics"

    return lyrics


def read_lyrics(path, files, lyrics_path=""):
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
        print(" X Lyrics file already exists:", folder)
    else:
        # Add the lyrics of every file in this folder to 'lyrics'.
        for file in files:
            file = path + file
            if os.path.isfile(file):
                lyrics += f"\n\n{'─'*120}\n\n  {file[len(path):-4]}\n\n\n"
                lyrics += load_lyrics(file) + "\n"
            elif os.path.isdir(file):
                inner_folders.append(file + "/")
        lyrics += "\n\n" + "─"*120 + "\n"

        # Save the lyrics text in a file.
        with open(lyrics_file, "w", encoding="utf-8") as lyricstxt:
            lyricstxt.write(lyrics)
        print(" Lyrics file generated:", folder)
        # print(lyrics)

    # Call the function again for folders inside this one.
    # Each folder will generate a separate lyrics text.
    for inner_path in inner_folders:
        read_lyrics(inner_path, sorted(os.listdir(inner_path)), lyrics_path)


def edit_lyrics(path, files):
    """Write the lyrics to a text file and then
    read back the edited version to the song and save it.
    """

    inner_folders = []

    for file in files:
        file = path + file

        if os.path.isfile(file):
            lyrics = load_lyrics(file)

            # Write the lyrics in the file in 'editor_path'.
            with open(editor_path, "w", encoding="utf-8") as lyricstxt:
                lyricstxt.write(lyrics)

            # Wait until edits are confirmed.
            if input(file.split("/")[-1] + " >< "):
                break

            # Read the edited lyrics from 'editor_path' file.
            with open(editor_path, "r", encoding="utf-8") as lyricstxt:
                lyrics = lyricstxt.read().strip()

            # Add the new lyrics to the song and save it.
            if file[-4:].lower() == ".mp3":
                tag = eyed3.load(file).tag
                tag.lyrics.set(lyrics)
                tag.save(version=eyed3.id3.ID3_V2_4, encoding="utf8")
            elif file[-4:].lower() == ".m4a":
                tag = MP4(file).tags
                tag["\xa9lyr"] = lyrics
                tag.save(file)

        elif os.path.isdir(file):
            inner_folders.append(file + "/")

    # Call the function again for folders inside this one.
    for inner_path in inner_folders:
        edit_lyrics(inner_path, sorted(os.listdir(inner_path)))


def format_path(path):
    path = path.strip(" '\"").replace("'\\''", "'").replace("\\", "/") + "/"
    path = re.sub("/+$", "/", path)
    return path


if __name__ == "__main__":

    print(
        "",
        "1.Set lyrics",
        "2.Create lyrics file",
        "3.Edit lyrics",
        "4.Search in lyrics",
        "5.Help",
        sep="\n ", end="",
    )
    choice = input("\n:")
    print("\n")

    # Print help.
    if choice == "5":
        with open("instructions.txt", "r") as instructions:
            print(instructions.read())
        raise SystemExit

    try:
        origin_path = format_path(input("\nEnter full path of the folder: "))
    except:
        raise SystemExit

    # TODO: this not so efficient, maybe os.getcwd() was good enough.
    realpath = os.path.realpath(__file__).replace("\\", "/")
    realpath = realpath[:realpath.rindex("/")]

    # If the input path is invalid,
    # create a folder called 'songs' in the current path
    # and use it as the 'origin_path'.
    if origin_path in ["/", "./", "//"] or not os.path.isdir(origin_path):
        origin_path = realpath + "/songs/"
        if not os.path.isdir(origin_path):
            os.mkdir(origin_path)

    # Get the list of all files in the 'origin_path'.
    origin_files = sorted(os.listdir(origin_path))
    if not origin_files:
        print("\n This folder is empty!\n")
        raise SystemExit


    # Search for lyrics in 'Genius.com' and add them to songs.
    if choice == "1":
        # genius = Genius(excluded_terms=["(Live)", "(Remix)"])
        genius = Genius()
        set_lyrics(origin_path, origin_files)
        print(
            f"\n\n\n successful: {added_lyrics}",
            f"\n unsuccessful: {not_added_lyrics}"
        )

    # For each folder, generate a text file containing all of its lyrics.
    elif choice == "2":
        lyrics_path = format_path(input("Lyrics files save location: "))
        print()
        read_lyrics(origin_path, origin_files, lyrics_path)

    # Lyrics editor.
    elif choice == "3":
        editor_path = realpath + "/lyrics_editor.txt"
        edit_lyrics(origin_path, origin_files)

    # Search for a phrase in lyrics files.
    elif choice == "4":
        search_lyrics(origin_path, origin_files)

    # Just for checking.
    elif choice == "6":
        print(origin_path)
        print(origin_files)

    print()
