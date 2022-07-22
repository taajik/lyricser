
import os

from song import Song
from utils import report


def auto_regularize(path, files, auto_names=True):
    """Automatically edit file name and some tags of songs."""

    print()
    if auto_names:
        folder = path.split("/")[-2].split(" - ")
        # If the folder consists of only one word,
        # it's used for both artist and album.
        artist = album = folder[0]
        # Otherwise, the album tag will be set to: "album - artist"
        if len(folder) != 1:
            album = folder[1] + " - " + artist
    else:
        artist = input(" artist: ").strip()
        album = input(" album: ").strip()

    inner_folders = []

    for file in files:
        report_message = file
        file = path + file

        if os.path.isfile(file):
            try:
                song = Song(file)
            except Exception as e:
                report(False, e)
                continue

            song.title = song.title.replace("’", "'").strip()
            song.album_artist = artist
            song.album = album
            song.track_num = song.track_num     # Delete total
            song.save()

            # Rename the song's file name.
            new_file = (
                f"{str(song.track_num or '  ').zfill(2).strip()} "
                f"{song.title}_{song.album_artist}.{song.ext}"
            )
            report_message += " => " + new_file
            new_file = path + new_file
            os.rename(file, new_file)
            report(True, report_message)

        elif os.path.isdir(file):
            inner_folders.append(file + "/")

    # Call the function again for folders inside this one.
    for inner_path in inner_folders:
        auto_regularize(inner_path, sorted(os.listdir(inner_path)), auto_names)
