
import os
import eyed3
import lyricsgenius


songs_path = "/" + input("Enter path of your musics folder: ").strip("/") + "/"

if not os.path.isdir(songs_path) or songs_path == "//":
    songs_path = os.getcwd() + "/songs/"
    if not os.path.isdir(songs_path):
        os.mkdir(songs_path)

without_lyrics_path = os.getcwd() + "/without_lyrics/"
if not os.path.isdir(without_lyrics_path):
    os.mkdir(without_lyrics_path)

files = sorted(os.listdir(songs_path))
if not files or songs_path=="//" or not songs_path:
    print("\n songs folder is empty!")
    exit()


def move_to_without_lyrics(file):
    mv = f"mv \"{file}\" \"{without_lyrics_path}\""
    if os.path.isfile(file) and not input(f" CONFIRM: {mv} "):
        os.system(mv)

added_lyrics = 0
def added():
    global added_lyrics
    added_lyrics += 1

not_added_lyrics = 0
def not_added(file=""):
    global not_added_lyrics
    not_added_lyrics += 1
    if file:
        move_to_without_lyrics(file)


client_access_token = 'JPmYaQ8e0nffrGMNZB-S2-5qxjAlVEb7YNtrGUG58PyCmy4jG5Z9pK2BN6kPZ6kW'
genius = lyricsgenius.Genius(client_access_token, skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"])
#genius = lyricsgenius.Genius(client_access_token, skip_non_songs=True, excluded_terms=["(Live)"])

def set_lyrics_auto(file):
    try:
        tag = eyed3.load(file).tag
    except:
        print(" X file not found:", file)
        not_added()
        return

    try:
        t = tag.title
        if '(' in t or ')' in t:
            print(t, "-", tag.album_artist)
            t = input("  t: ")
            if not t.strip():
                t = tag.title
        lyrics = genius.search_song(t, tag.album_artist, get_full_info=False).lyrics
        #lyrics = genius.search_song(song_id=, get_full_info=False).lyrics
        #lyrics = """"""
    except:
        print(" X lyrics not found:", file)
        not_added(file)
        return

    try:
        tag.lyrics.set(lyrics.strip())
        tag.save(version=eyed3.id3.ID3_V2_4, encoding="utf8")
        added()
        return
    except:
        print(" X lyrics not added:", file)
        not_added(file)
        return


def set_auto(path, files):
    print("\n" + "─"*len(path) + "──┐")
    print(" " + path + " │", len(files))
    print("─"*len(path) + "──┘")

    files2 = []
    i = 0
    for file in files:
        file = path + file
        if os.path.isfile(file):
            i += 1
            print('\n', i, end=": ")
            set_lyrics_auto(file)
        elif os.path.isdir(file):
            files2.append(file + '/')

    for path2 in files2:
        set_auto(path2, sorted(os.listdir(path2)))


def see_lyrics(path, files): # NOTE: needs a review or maybe just remove it all
    print("\n" + "┌─" + "─"*len(path) + "─┐")
    print("│ " + path + " │")
    print("└─" + "─"*len(path) + "─┘")
    print("\n" + "─"*os.get_terminal_size()[0])
    files2 = []
    for file in files:
        file = path + file
        if os.path.isfile(file):
            try:
                print("\n\n  ", files.index(file[len(path):])+1, "/", len(files), sep="",  end = " ")
                print(file[len(path):-4] + "\n\n")
                tag = eyed3.load(file).tag
                if len(tag.lyrics):
                    print(tag.lyrics[0].text)
            except:
                print("    file not found:", file[len(path):])
            print("\n\n" + "─"*os.get_terminal_size()[0])
        elif os.path.isdir(file):
            files2.append(file + '/')

    for path2 in files2:
        see_lyrics(path2, sorted(os.listdir(path2)))

def search_lyrics(path, files):
    lyrics_file = open("lyrics.txt", "w")
    lyrics = ""
    for file in files:
        file = path + file
        if os.path.isfile(file):
            try:
                tag = eyed3.load(file).tag
                lyrics += tag.lyrics[0].text
            except:
                print("    file not found:", file[len(path):])
    lyrics_file.write(lyrics)

sss = input(" 1.Set lyrics\n 2.See lyrics\n:")
print()
if sss == '1':
    set_auto(songs_path, files)
    print("\n\n successfulls:", added_lyrics, "\n unsuccessfulls:", not_added_lyrics)
elif sss == '2':
    see_lyrics(songs_path, files)
elif sss == '2':
    search_lyrics(songs_path, files)
print()
