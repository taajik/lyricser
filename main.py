
import argparse

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

regularize_parser = subparsers.add_parser("regularize", help="Auto regularize songs")
add_common_arguments(regularize_parser)

set_parser = subparsers.add_parser("set", help="Set lyrics on songs")
add_common_arguments(set_parser)

create_parser = subparsers.add_parser("create", help="Create lyrics files from lyrics of songs")
add_common_arguments(create_parser)

edit_parser = subparsers.add_parser("edit", help="Edit lyrics of songs")
add_common_arguments(edit_parser)

search_parser = subparsers.add_parser("search", help="Search inside all lyrics files")
add_common_arguments(search_parser)


if __name__ == "__main__":

    args = parser.parse_args()
    print(args)

    print(
        "",
        "1.Help",
        "2.Auto regularize songs",
        "3.Set lyrics",
        "4.Create lyrics files",
        "5.Edit lyrics",
        "6.Search in lyrics",
        sep="\n ", end="",
    )
    #choice = input("\n:")

    raise SystemExit

    # Print help without asking for path to the folder.
    if choice == "1":
        with open("instructions.txt") as instructions:
            print(instructions.read())
        raise SystemExit

    try:
        origin_path = input("\nEnter full path of the folder: ")
    except:
        raise SystemExit
    print("\n")
    origin_path = utils.format_path(origin_path)

    if not utils.is_valid_dir(origin_path):
        print("\n Invalid path!\n")
        raise SystemExit
    if not next(origin_path.iterdir(), None):
        print("\n This folder is empty!\n")
        raise SystemExit

    # Regularize songs' tags
    if choice == "2":
        auto_names = input(
            "Extract artist and album names "
            "from the folder's name? (Y or n): "
        ).lower()
        print()
        auto_regularize(origin_path, auto_names!="n")
        utils.print_report("modified", "not modified")

    # Search for lyrics in 'Genius.com' and add them to songs.
    elif choice == "3":
        is_album = input("Is each folder an album? (Y or n): ").lower()
        print()
        # genius = Genius(excluded_terms=["(Live)", "(Remix)"])
        genius = Genius()
        auto_add_lyrics(origin_path, genius, is_album!="n")
        utils.print_report("added", "not added")

    # For each folder, generate a text file containing all of its lyrics.
    elif choice == "4":
        lyrics_path = utils.format_path(input("Lyrics files save location: "))
        print()
        if utils.is_valid_dir(lyrics_path):
            create_lyrics_file(origin_path, lyrics_path)
        else:
            create_lyrics_file(origin_path)
        utils.print_report("created", "not created")

    # Lyrics editor.
    elif choice == "5":
        edit_lyrics(origin_path)

    # Search for a phrase in lyrics files.
    elif choice == "6":
        q = input("Search phrase: ").lower()
        print()
        if len(q) < 3:
            print(" X It's too short (three characters minimum)")
        else:
            search_lyrics(origin_path, q)

    # Just for checking.
    elif choice == "0":
        print(origin_path)

    print()
