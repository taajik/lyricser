
from file_regularization import auto_regularize
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
        "2.Auto regularize songs",
        "3.Set lyrics",
        "4.Edit lyrics",
        "5.Create lyrics files",
        "6.Search in lyrics",
        sep="\n ", end="",
    )
    choice = input("\n:")

    # Print help without asking for path to the folder.
    if choice == "1":
        with open("instructions.txt", "r") as instructions:
            print(instructions.read())
        raise SystemExit

    try:
        origin_path = input("\nEnter full path of the folder: ")
    except:
        raise SystemExit
    print("\n")
    origin_path, origin_files = utils.setup(origin_path)

    # Regularize songs' tags
    if choice == "2":
        auto_names = input(
            "Extract artist and album names "
            "from the folder's name? (Y or n): "
        ).lower()
        auto_regularize(origin_path, origin_files, auto_names != "n")
        utils.print_report("modified", "not modified")

    # Search for lyrics in 'Genius.com' and add them to songs.
    elif choice == "3":
        from lyrics_attachment import auto_add_lyrics
        auto_add_lyrics(origin_path, origin_files)
        utils.print_report("added", "not added")

    # Lyrics editor.
    elif choice == "4":
        edit_lyrics(origin_path, origin_files)

    # For each folder, generate a text file containing all of its lyrics.
    elif choice == "5":
        lyrics_path = utils.format_path(input("Lyrics files save location: "))
        print()
        create_lyrics_file(origin_path, origin_files, lyrics_path)
        utils.print_report("created", "not created")

    # Search for a phrase in lyrics files.
    elif choice == "6":
        search_lyrics(origin_path, origin_files)

    # Just for checking.
    elif choice == "0":
        print(origin_path)
        print(origin_files)

    print()
