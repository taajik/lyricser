
import argparse
import os

from lyricsgenius import Genius

from file_regularization import auto_regularize
from lyrics_attachment import auto_add_lyrics
from lyrics_manipulation import (
    create_lyrics_file,
    edit_lyrics,
    search_lyrics,
)
import utils


parser = argparse.ArgumentParser(description="Edit and add lyrics to your songs.")
subparsers = parser.add_subparsers(title="Commands", dest="command", metavar="")

def add_common_arguments(parser):
    parser.add_argument("-r", "--recursive", action="store_true",
                        help="recursive files search from provided root path")
    parser.add_argument("path", type=str)

regularize_parser = subparsers.add_parser("regular", help="Auto regularize songs")
add_common_arguments(regularize_parser)
regularize_parser.add_argument("-a", "--auto-names", action="store_true", help="extract artist and album names from the folder's name")
regularize_parser.add_argument("-n", "--no-rename", action="store_false", dest="rename", help="do not change songs' file names (only edit tags)")

set_parser = subparsers.add_parser("set", help="Add lyrics to songs")
add_common_arguments(set_parser)
set_parser.add_argument("-i", "--is-album", action="store_true", help="consider all songs in a folder as an album")

create_parser = subparsers.add_parser("create", help="Create lyrics files from lyrics of songs")
add_common_arguments(create_parser)

edit_parser = subparsers.add_parser("edit", help="Edit lyrics of songs")
add_common_arguments(edit_parser)

search_parser = subparsers.add_parser("search", help="Search inside all lyrics files")
add_common_arguments(search_parser)


if __name__ == "__main__":

    args = parser.parse_args()
    # print(args)

    # Print help if the program is run without any arguments.
    if args.command is None:
        parser.print_help()
        raise SystemExit

    assert hasattr(args, "path"), "path argument is required"
    origin_path = utils.format_path(args.path)
    if not utils.is_valid_dir(origin_path):
        print(" X Error: Invalid path!")
        raise SystemExit
    if not next(origin_path.iterdir(), None):
        print(" X Error: The folder is empty!")
        raise SystemExit

    # Regularize songs' tags and filename
    if args.command == "regular":
        auto_regularize(origin_path, args.recursive, args.auto_names, args.rename)
        utils.print_report("modified", "not modified")

    # Search for lyrics in 'Genius.com' and add them to songs.
    elif args.command == "set":
        # genius = Genius(excluded_terms=["(Live)", "(Remix)"])
        genius = Genius(os.environ.get("API_TOKEN"), verbose=False)
        album = auto_add_lyrics(origin_path, genius, args.recursive, args.is_album)
        utils.print_report("added", "not added")

    # For each folder, generate a text file containing all of its lyrics.
    elif args.command == "create":
        lyrics_path = utils.format_path(input("Lyrics files save location: "))
        print()
        if utils.is_valid_dir(lyrics_path):
            create_lyrics_file(origin_path, lyrics_path)
        else:
            create_lyrics_file(origin_path)
        utils.print_report("created", "not created")

    # Songs' lyrics editor.
    elif args.command == "edit":
        edit_lyrics(origin_path)

    # Search for a phrase in lyrics files.
    elif args.command == "search":
        q = input("Search phrase: ").lower()
        print()
        if len(q) < 3:
            print(" X It's too short (three characters minimum)")
        else:
            search_lyrics(origin_path, q)

    print()
