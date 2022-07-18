
from lyrics_manipulation import (
    create_lyrics_file,
    edit_lyrics,
    search_lyrics,
)
import utils


if __name__ == "__main__":

    print(
        "",
        "1.Help",
        "2.Set lyrics",
        "3.Create lyrics files",
        "4.Edit lyrics",
        "5.Search in lyrics",
        sep="\n ", end="",
    )
    choice = input("\n:")
    print("\n")

    # Print help without asking for path to the folder.
    if choice == "1":
        with open("instructions.txt", "r") as instructions:
            print(instructions.read())
        raise SystemExit

    try:
        origin_path = input("\nEnter full path of the folder: ")
    except:
        raise SystemExit
    origin_path, origin_files = utils.setup(origin_path)

    # Search for lyrics in 'Genius.com' and add them to songs.
    if choice == "2":
        from .add_lyrics import set_lyrics
        set_lyrics(origin_path, origin_files)
        utils.print_report("added", "not added")

    # For each folder, generate a text file containing all of its lyrics.
    elif choice == "3":
        lyrics_path = utils.format_path(input("Lyrics files save location: "))
        print()
        create_lyrics_file(origin_path, origin_files, lyrics_path)
        utils.print_report("created", "not created")

    # Lyrics editor.
    elif choice == "4":
        edit_lyrics(origin_path, origin_files)

    # Search for a phrase in lyrics files.
    elif choice == "5":
        search_lyrics(origin_path, origin_files)

    # Just for checking.
    elif choice == "6":
        print(origin_path)
        print(origin_files)

    print()
