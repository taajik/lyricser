
import os
import re

from song import Song
from utils import report, print_header


def get_file_name(song: Song):
    """Make up the song's file name according to its tags."""

    # Extract parentheses from the title.
    title = song.title
    parens = re.search(" \(.*\)", title)
    if parens is not None:
        parens = parens.group()
        title = title.replace(parens, "")

    # Find other artists from the 'artists' tag.
    artists = song.artists.split(", ")
    artists.remove(song.album_artist)
    if artists:
        print(" Collaborator artists found:", artists)
        set_as_feat = input("  Set as featured? (Y or n): ").lower()
        if set_as_feat != "n":
            artists = " (ft. " + " & ".join(artists) + ")"
        else:
            artists = "_" + "_".join(artists)

    new_file = (
        f"{str(song.track_num or '  ').zfill(2)} "
        f"{title}_{song.album_artist}{artists or ''}{parens or ''}.{song.format}"
    )
    return new_file.strip()


def auto_regularize(path, files, auto_names=True):
    """Automatically edit file name and some tags of songs."""

    print_header(path, files)

    if auto_names:
        folder = path.split("/")[-2].split(" - ")
        # If the folder consists of only one word,
        # it's used for both artist and album.
        artist = album = folder[0]
        # Otherwise, the album tag will be set to: "album - artist"
        if len(folder) != 1:
            album = folder[1] + " - " + artist
    else:
        artist = input(" artist: ")
        album = input(" album: ")
        print()
    artist = artist.strip()
    album = album.strip()

    inner_folders = []

    for file in files:
        file_path = path + file

        if os.path.isfile(file_path):
            print(file)
            try:
                song = Song(file_path)
            except Exception as e:
                report(False, e)
                continue

            song.title = song.title.replace("’", "'").strip()
            if artist:
                song.album_artist = artist
            if album:
                song.album = album
            song.track_num = song.track_num     # Delete the total
            song.save()

            # Rename the song's file name.
            new_file = get_file_name(song)
            new_file_path = path + new_file
            if new_file_path != file_path:
                os.rename(file_path, new_file_path)
                report(True, new_file)
            else:
                report(False, "Same!")
            print()

        elif os.path.isdir(file_path):
            inner_folders.append(file_path + "/")

    # Call the function again for folders inside this one.
    for inner_path in inner_folders:
        auto_regularize(inner_path, sorted(os.listdir(inner_path)), auto_names)
