
import os
import eyed3
from mutagen.mp4 import MP4
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
not_added_lyrics = 0
def add(i, file=""):
    global added_lyrics
    global not_added_lyrics
    if i:
        added_lyrics += 1
    else:
        not_added_lyrics += 1
        if file:
            move_to_without_lyrics(file)


client_access_token = 'JPmYaQ8e0nffrGMNZB-S2-5qxjAlVEb7YNtrGUG58PyCmy4jG5Z9pK2BN6kPZ6kW'
genius = lyricsgenius.Genius(client_access_token, skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"])
# genius = lyricsgenius.Genius(client_access_token, skip_non_songs=True, excluded_terms=["(Live)"])

def set_lyrics_mp3(file):
    try:
        tag = eyed3.load(file).tag
    except:
        print(" X file not found:", file)
        add(False)
        return

    try:
        t = tag.title
        aa = tag.album_artist
        if '(' in t or ')' in t:
            print(t, "-", aa)
            t = input("  t: ")
            if not t.strip():
                t = tag.title
        lyrics = genius.search_song(t, aa, get_full_info=False).lyrics
        # lyrics = genius.search_song(song_id=, get_full_info=False).lyrics
        # lyrics = """"""
    except:
        print(" X lyrics not found:", file)
        add(False, file)
        return

    try:
        tag.lyrics.set(lyrics.strip())
        tag.save(version=eyed3.id3.ID3_V2_4, encoding="utf8")
        add(True)
        return
    except:
        print(" X lyrics not added:", file)
        add(False, file)
        return


def set_lyrics_m4a(file):
    try:
        tags = MP4(file).tags
        t = tags.get('\xa9nam')
        aa = tags.get('aART')
        if len(t) == 1 and len(aa) == 1:
            t = t[0]
            aa = aa[0]
        else:
            print(t, "-", aa)
            t = input("  t: ")
            aa = input(" aa: ")
        if '(' in t or ')' in t:
            print(t, "-", aa)
            t = input("  t: ")
            if not t.strip():
                t = tags.get('\xa9nam')[0]
    except:
        print(" X File Error:", file)
        add(False)
        return

    try:
        lyrics = genius.search_song(t, aa, get_full_info=False).lyrics
        # lyrics = genius.search_song(song_id=, get_full_info=False).lyrics
        # lyrics = """"""
        tags['\xa9lyr'] = lyrics
        tags.save(file)
        add(True)
        return
    except:
        print(" X Lyrics Error:", file)
        add(False, file)
        return


def set_lyrics(path, files):
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
            if file[-4:].lower() == ".m4a":
                set_lyrics_m4a(file)
            else:
                set_lyrics_mp3(file)

        elif os.path.isdir(file):
            files2.append(file + '/')

    for path2 in files2:
        set_lyrics(path2, sorted(os.listdir(path2)))


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
                if file[-4:].lower() == ".m4a":
                    print(MP4(file).tags.get("\xa9lyr")[0])
                else:
                    print(eyed3.load(file).tag.lyrics[0].text)
            except:
                print("    file not found:", file[len(path):])
            print("\n\n" + "─"*os.get_terminal_size()[0])
        elif os.path.isdir(file):
            files2.append(file + '/')

    for path2 in files2:
        see_lyrics(path2, sorted(os.listdir(path2)))

def find_without_lyrics(path, files):
    print(path)
    files2 = []
    for file in files:
        file = path + file
        if os.path.isfile(file):
            try:
                if file[-4:].lower() == ".m4a":
                    if not MP4(file).tags.get("\xa9lyr")[0]:
                        raise Exception
                else:
                    if not eyed3.load(file).tag.lyrics[0].text.strip():
                        raise Exception
            except:
                print(file[len(path):])
        elif os.path.isdir(file):
            files2.append(file + '/')
    for path2 in files2:
        find_without_lyrics(path2, sorted(os.listdir(path2)))

sss = input(" 1.Set lyrics\n 2.See lyrics\n:")
print()
if sss == '1':
    print('\n', songs_path)
    if not input(" SET LYRICS? ").split():
        set_lyrics(songs_path, files)
        print(f"\n\n\n successfulls: {added_lyrics} \n unsuccessfulls: {not_added_lyrics}")
elif sss == '2':
    see_lyrics(songs_path, files)
elif sss == '3':
    find_without_lyrics(songs_path, files)
print()
