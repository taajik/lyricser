
import re

from song import Song
from utils import report, get_header


def get_file_name(song: Song):
    """Make up the song's file name according to its tags."""

    # Extract parentheses from the title.
    title = song.title
    title = re.sub(" ?/+ ?", " - ", title)
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


def auto_regularize(path, auto_names=True):
    """Automatically edit file name and some tags of songs."""

    print(get_header(path))
    inner_folders = []

    if auto_names:
        folder = path.name.split(" - ")
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

    for file in path.iterdir():
        if file.is_file():
            print(file.name)
            try:
                song = Song(file)
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
            new_file = path / get_file_name(song)
            if file.name != new_file.name:
                file.replace(new_file)
                report(True, new_file.name)
            else:
                report(False, "Same!")
            print()

        elif file.is_dir():
            inner_folders.append(file)
    print()

    # Call the function again for folders inside this one.
    for inner_path in inner_folders:
        auto_regularize(inner_path, auto_names)
