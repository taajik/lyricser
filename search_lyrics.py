

def search_lyrics(path, files):
    ## searching in all of the lyrics files generated by read_lyrics function

    q = input("Search query: ").lower()
    print()
    if len(q) < 4:
        print(" X It's too short (four characters minimum)")
        return

    ## for every txt file in the folder
    for album in files:

        if album[-4:].lower() != ".txt":
            continue

        file = open(path + album, 'r')
        txt = file.read()
        ## separating each songs lyrics as elements of a list
        txt = txt.split('─' * 120)[1:-1]

        for song in txt:
            ## if there was a match
            if q in song.lower():
                ## printing the name of the file and song in which the match is
                print(album, song.splitlines()[2])

        file.close()


if __name__ == "__main__":
    import os

    lyrics_path = input("\nEnter the path of your lyrics folder: ")
    lyrics_files = sorted(os.listdir(lyrics_path))
    print()

    search_lyrics(lyrics_path, lyrics_files)
    print()

