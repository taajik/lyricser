
from song import Song
from utils import report, get_header


def create_lyrics_file(path, lyrics_path=None, recursive=False):
    """Generate a text containing lyrics of all the songs in a folder."""

    lyrics_file = path
    if lyrics_path:
        lyrics_file = lyrics_path
    lyrics_file /= path.name + " (Lyrics).txt"
    lyrics = get_header(path, full_path=False) + "\n"
    inner_folders = []

    if lyrics_file.exists():
        report(False, " X Lyrics file already exists: " + lyrics_file.name)
    else:
        # Add the lyrics of every file in this folder to 'lyrics'.
        for file in sorted(path.iterdir()):
            if file.is_file():
                lyrics += f"\n\n{'─'*120}\n\n  {file.stem}\n\n\n"
                try:
                    lyrics += Song(file).lyrics
                except Exception as e:
                    print(e)
                lyrics += "\n"
            elif file.is_dir():
                inner_folders.append(file)

        lyrics += "\n\n" + "─"*120 + "\n"
        # Save the lyrics text in a file.
        with open(lyrics_file, "w", encoding="utf-8") as lyricstxt:
            lyricstxt.write(lyrics)
        report(True, " Lyrics file generated: " + lyrics_file.name)
        # print(lyrics)

    # Call the function again for folders inside this one.
    # Each folder will generate a separate lyrics text.
    if recursive:
        for inner_path in inner_folders:
            create_lyrics_file(inner_path, lyrics_path, recursive)


def edit_lyrics(path, recursive=False):
    """Write the lyrics to a text file and then
    read back the edited version to the song and save it.
    """

    print(get_header(path))
    inner_folders = []

    for file in sorted(path.iterdir()):
        if file.is_file():
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
            try:
                # Entering 'n' will skip this song.
                if input(f"{file.name:<50}\t Edited? ") == "n":
                    continue
            except KeyboardInterrupt:
                raise SystemExit

            # Read the edited lyrics from the editor file.
            with open("lyrics_editor.txt", "r", encoding="utf-8") as lyricstxt:
                lyrics = lyricstxt.read().strip()

            # Add the new lyrics to the song and save it.
            song.lyrics = lyrics
            song.save()

        elif file.is_dir():
            inner_folders.append(file)

    # Call the function again for folders inside this one.
    if recursive:
        for inner_path in inner_folders:
            edit_lyrics(inner_path, recursive)


def search_lyrics(path, q):
    """Search for a phrase in all of the lyrics files
    inside the entered folder.

    The results lists the song and file names that include the phrase.
    """

    inner_folders = []

    for file in sorted(path.iterdir()):
        if file.is_file():
            if file.suffix.lower() != ".txt":
                continue

            with open(file, "r", encoding="utf-8") as txt_file:
                lyrics = txt_file.read()
            # Split the full lyrics file into separate song lyrics.
            lyrics = lyrics.split("─" * 120)[1:-1]

            for song in lyrics:
                if q in song.lower():
                    # For each match, print the song name
                    print(file.name, song.splitlines()[2])

        elif file.is_dir():
            inner_folders.append(file)

    # Call the function again for folders inside this one.
    for inner_path in inner_folders:
        search_lyrics(inner_path, q)
