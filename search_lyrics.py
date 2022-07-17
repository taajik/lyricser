
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


if __name__ == "__main__":
    import os
    import re

    lyrics_path = input("\nEnter the path of your lyrics folder: ").replace("\\", "/")
    lyrics_path = re.sub("/*$", "/", lyrics_path)
    lyrics_files = sorted(os.listdir(lyrics_path))
    print()

    search_lyrics(lyrics_path, lyrics_files)
    print()
